from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from src.exams.models import Exam, Question, Choice
from src.exams.serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer, ExamChoiceSerializer


class ExamViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.CreateModelMixin, mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Creates, Updates and Retrieves - Exams
    """
    queryset = Exam.objects.all()
    serializers = {
        'default': ExamSerializer,
    }

    def get_serializer_class(self):
        if self.action in ['submit_exam']:
            return ExamChoiceSerializer
        return self.serializers.get(self.action, self.serializers['default'])

    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='submitExam', url_name='submitExam')
    def submit_exam(self, request, pk):
        score = Choice.objects.filter(id__in=request.data.get('choices'), correct_answer=True, question__exam=pk).count()

        serializer = self.get_serializer(data={
            'exam': self.get_object(),
            'user': request.user,
            'score': score
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


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


class ChoiceViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
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
