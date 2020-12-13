from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from src.exams.models import Exam, Question, Choice, Domain, Problem, Subject
from src.exams.serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer, ExamResultSerializer, DomainSerializer, \
    SubjectSerializer, CreateExamSerializer
from src.users.models import User
class ExamViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Creates, Updates and Retrieves - Exams
    """
    queryset = Exam.objects.all()
    serializers = {
        'default': ExamSerializer,
        'create': CreateExamSerializer
    }

    def get_serializer_class(self):
        if self.action in ['submit_exam']:
            return ExamResultSerializer
        return self.serializers.get(self.action, self.serializers['default'])

    def get_queryset(self):
        if self.request.user.is_teacher:
            return self.queryset.filter(subject__teacher=self.request.user)
        elif self.request.user.is_student:
            return self.queryset.filter(subject__students=self.request.user)
        else:
            return self.queryset.none()

    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='submitExam', url_name='submitExam')
    def submit_exam(self, request, pk):
        choices_ids = request.data.get('choices')
        score = Choice.objects.filter(id__in=choices_ids, correct_answer=True, question__exam=pk).count()

        serializer = self.get_serializer(data={
            'exam': self.get_object(),
            'user': request.user,
            'score': score,
            'choices': choices_ids
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        maximum_score = Choice.objects.filter(correct_answer=True, question__exam=pk).count()

        if maximum_score / 2 < score:
            self.request.user.passed_exams.add(self.get_object())

        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, mixins.CreateModelMixin):
    """
        Lists, Retrieves, Creates - Subjects
    """

    queryset = Subject.objects.all()
    serializers = {
        'default': SubjectSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    permission_classes = [IsAuthenticated]


class QuestionViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      mixins.CreateModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
        Creates, Updates and Retrieves - Questions
        """
    queryset = Question.objects.all()
    serializers = {
        'default': QuestionSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    permission_classes = [IsAuthenticated]


class ChoiceViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.CreateModelMixin, mixins.ListModelMixin):
    """
        Creates, Updates and Retrieves - Choices
        """
    queryset = Choice.objects.all()
    serializers = {
        'default': ChoiceSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    permission_classes = [IsAuthenticated]


class DomainViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                    mixins.ListModelMixin, mixins.DestroyModelMixin):
    """
    List and Retrieve - Domains
    """
    queryset = Domain.objects.all()
    serializers = {
        'default': DomainSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_queryset(self):
        if self.request.user.is_teacher:
            return self.queryset.filter(subject__teacher=self.request.user)
        elif self.request.user.is_student:
            return self.queryset.filter(subject__students=self.request.user)
        else:
            return self.queryset.none()

    @action(detail=True, methods=['get'], url_path='personalized_exams')
    def personalized_problems(self, request, pk):
        nodes_to_check = list(self.queryset.get(pk=pk).problems.all())
        nodes_to_return = []

        while(len(nodes_to_check)):
            current_node = nodes_to_check.pop()
            if self.request.user.passed_exams.filter(problem=current_node).exists():
                nodes_to_check += Problem.objects.filter(pk__in=current_node.target_problems.all().values_list('target'))
            else:
                nodes_to_return.append(current_node.exam)

        return Response(ExamSerializer(nodes_to_return, many=True).data)

    @action(detail=True, methods=['patch'], url_path='add-student')
    def add_student(self, request, pk):
        self.get_object().subject.students.add(User.objects.get(pk=request.data.get('id')))
        return HttpResponse('')
