import numpy as np

from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


from src.exams.models import Exam, Question, Choice, Domain, Problem, Subject, ProblemAttachment, ExamResult
from src.exams.serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer, CreateExamResultSerializer, \
    DomainSerializer, SubjectSerializer, CreateExamSerializer, ProblemAttachmentSerializer, ProblemSerializer
from src.users.models import User
from src.users.serializers import UserSerializer

from learning_spaces.kst.iita import iita


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
            return CreateExamResultSerializer
        return self.serializers.get(self.action, self.serializers['default'])

    def get_queryset(self):
        if self.request.user.is_teacher:
            return self.queryset.filter(subject__teacher=self.request.user)
        elif self.request.user.is_student:
            return self.queryset.filter(subject__students=self.request.user)
        else:
            return self.queryset.none()

    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='examTakers', url_name='examTakers')
    def exam_takers(self, request, pk):
        user_ids = ExamResult.objects.filter(exam=self.get_object()).values_list('user', flat=True)
        return Response(UserSerializer(User.objects.filter(pk__in=user_ids), many=True).data)

    @action(detail=True, methods=['get'], url_path='generateKnowledgeSpace', url_name='generateKnowledgeSpace')
    def generate_knowledge_space(self, request, pk):
        exam = self.get_object()
        user_ids = ExamResult.objects.filter(exam=self.get_object()).values_list('user', flat=True)

        correct_answers_matrix = []
        for user in user_ids:
            user_questions_array = []
            for question in exam.questions.all().order_by('id'):
                should_be_true_answers = question.choices.filter(correct_answer=True).values_list('id', flat=True)
                should_be_false_answers = question.choices.filter(correct_answer=False).values_list('id', flat=True)

                correct_answer = ExamResult.objects.filter(
                    user__id=user, exam=exam, choices__in=should_be_true_answers
                ).exclude(choices__in=should_be_false_answers).exists()

                question_value = 1 if correct_answer else 0
                user_questions_array.append(question_value)

            correct_answers_matrix.append(user_questions_array)

        ks = iita(np.array([np.array(questions_array) for questions_array in correct_answers_matrix]), 1)

        print(ks)

        return Response()

    @action(detail=True, methods=['post'], url_path='submitExam', url_name='submitExam')
    def submit_exam(self, request, pk):
        choices_ids = request.data.get('choices')
        score = Choice.objects.filter(id__in=choices_ids, correct_answer=True, question__exam=pk).count()

        serializer = self.get_serializer(data={
            'exam': self.get_object().id,
            'user': request.user.id,
            'score': score,
            'choices': choices_ids
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        maximum_score = Choice.objects.filter(correct_answer=True, question__exam=pk).count()

        if maximum_score / 2 < score:
            self.request.user.passed_exams.add(self.get_object())

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='getUnattachedExamsForDomainId')
    def get_unattached_exams_for_domain_id(self, request, pk):
        """
        get ids of exams that aren't attached to a problem
        """
        exams = [{"id": exam["id"], "title": exam["title"]} for exam in list(Exam.objects.filter(subject_id=pk).values())]
        attached_exams_ids = [problem["exam_id"] for problem in list(Problem.objects.filter(domain_id=pk).values())]
        unattached_exams = []
        for exam in exams:
            id = exam["id"]
            if id not in attached_exams_ids:
                unattached_exams.append(exam)

        return Response(unattached_exams)


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
    def personalized_exams(self, request, pk):
        nodes_to_check = list(self.queryset.get(pk=pk).problems.all())
        nodes_to_return = []

        while len(nodes_to_check):
            current_node = nodes_to_check.pop()
            if self.request.user.passed_exams.filter(problem=current_node).exists():
                nodes_to_check += Problem.objects.filter(
                    pk__in=current_node.target_problems.all().values_list('target'))
            else:
                nodes_to_return.append(current_node.exam)

        return Response(ExamSerializer(nodes_to_return, many=True).data)


class ProblemAttachmentViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                               mixins.CreateModelMixin, mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    queryset = ProblemAttachment.objects.all()
    serializers = {
        'default': ProblemAttachmentSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    permission_classes = [IsAuthenticated]

    def is_cyclic_util(self, node, visited, recursion_stack, nodes, index):
        # Mark current node as visited and
        # adds to recursion stack
        visited[index] = True
        recursion_stack[index] = True

        # Recur for all neighbors
        # if any neighbor is visited and in
        # recStack then graph is cyclic

        for neighbor in node["neighbors"]:
            idx = 0
            neighbor_node = {}
            # neighbor has to be full node, not just index
            for i in range(len(nodes)):
                if nodes[i]['id'] == neighbor:
                    idx = i
                    neighbor_node = nodes[i]
                    break
            if not visited[idx]:

                if self.is_cyclic_util(neighbor_node, visited, recursion_stack, nodes, idx):
                    return True
            elif recursion_stack[idx]:
                return True

        # The node needs to be popped from
        # recursion stack before function ends
        recursion_stack[index] = False
        return False

    def is_cyclic(self, nodes):
        visited = [False] * len(nodes)
        recursion_stack = [False] * len(nodes)

        for i in range(len(nodes)):
            if not visited[i]:
                if self.is_cyclic_util(nodes[i], visited, recursion_stack, nodes, i):
                    return True
        return False

    @action(detail=False, methods=['post'], url_path='custom_create', url_name='custom_create')
    def custom_make(self, request):
        new_problem_attachment = {"source": request.data["source"], "target": request.data["target"]}
        problem_attachments = list(ProblemAttachment.objects.all())
        node_lst = list(Domain.objects.get(pk=request.data["domainId"]).problems.all())
        nodes = []
        # set up nodes
        for node in node_lst:
            node_obj = {'id': node.id, 'neighbors': []}

            for p_a in problem_attachments:
                if p_a.source.id == new_problem_attachment["source"] and \
                        p_a.target.id == new_problem_attachment["target"]:
                    return Response("Failure - link already exists")
                if p_a.source.id == node.id:
                    node_obj['neighbors'].append(p_a.target.id)
            nodes.append(node_obj)

        for node in nodes:
            if node['id'] == new_problem_attachment['source']:
                node['neighbors'].append(new_problem_attachment['target'])

        if not self.is_cyclic(nodes):
            serializer = self.get_serializer(data={
                'source': new_problem_attachment["source"],
                'target': new_problem_attachment["target"]
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(request.data)
        return Response("Failure - this would create a cyclic graph")


class ProblemViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.CreateModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Problem.objects.all()
    serializers = {
        'default': ProblemSerializer,
    }
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @action(detail=False, methods=['post'], url_path='custom_create', url_name='custom_create')
    def custom_make(self, request):
        new_problem_id = Problem.objects.all().count() + 1
        new_problem = {"id": new_problem_id, "title": request.data["title"], "exam": request.data["examId"],
                       "domain": request.data["domainId"], "attached": []}
        serializer = self.get_serializer(data=new_problem)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)

    @action(detail=True, methods=['patch'], url_path='add-student')
    def add_student(self, request, pk):
        self.get_object().subject.students.add(User.objects.get(pk=request.data.get('id')))
        return HttpResponse('')
