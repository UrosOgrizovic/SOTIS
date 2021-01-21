import numpy as np

from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from django.conf import settings

from src.exams.models import Exam, Question, Choice, Domain, Problem, Subject, ProblemAttachment, ExamResult, \
    ActualProblemAttachment, DiffProblemAttachment, GraphEditDistance
from src.exams.serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer, CreateExamResultSerializer, \
    DomainSerializer, SubjectSerializer, CreateExamSerializer, ProblemAttachmentSerializer, ProblemSerializer, \
    GraphEditDistanceSerializer
from src.exams.helpers import is_cyclic, generate_knowledge_states,\
    determine_next_question, \
    order_questions_actual, order_questions_expected,\
    update_likelihoods_for_current_state, guess_current_state, update_likelihoods_markov
from src.users.models import User
from src.users.serializers import UserSerializer
from src.users.permissions import IsTeacherUser, IsStudentUser
from src.config.celery import generate_iita

from learning_spaces.kst.iita import iita
# from Levenshtein import distance as levenshtein_distance
import networkx as nx


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

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsTeacherUser]
        else:
            self.permission_classes = [IsAuthenticated]

        return super(ExamViewSet, self).get_permissions()

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

    @action(detail=True, methods=['get'], url_path='examTakers', url_name='examTakers')
    def exam_takers(self, request, pk):
        '''
            Returns users that partook a specific exam.
        '''
        user_ids = ExamResult.objects.filter(exam=self.get_object()).values_list('user', flat=True)
        return Response(UserSerializer(User.objects.filter(pk__in=user_ids), many=True).data)

    @action(detail=True, methods=['get'], url_path='generateKnowledgeSpace', url_name='generateKnowledgeSpace')
    def generate_knowledge_space(self, request, pk):
        '''
            Generates knowledge space for a particular exam.
            It creates a matrix of correct and uncorrect answers which is passed as input to IITA algorithm.
            Results are gathered asynchronously and saved in database.
        '''

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

        if settings.ENABLE_ASYNC:
            generate_iita.delay(correct_answers_matrix, exam.id)
            return HttpResponse('')

        ks = iita(np.array([np.array(questions_array) for questions_array in correct_answers_matrix]), 1)

        implications = ks.get('implications', [])
        for source_id, target_id in implications:
            question_source = exam.questions.all().order_by('id')[source_id]
            question_target = exam.questions.all().order_by('id')[target_id]

            ActualProblemAttachment.objects.get_or_create(source=question_source.problem,
                                                          target=question_target.problem)
        self.compare_knowledge_spaces(request, pk)
        return HttpResponse('')

    @action(detail=True, methods=['get'], url_path='compareKnowledgeSpaces', url_name='compareKnowledgeSpaces')
    def compare_knowledge_spaces(self, request, pk):
        '''
            Compares expected and actual knowledge spaces using networkx library.
        '''
        exam = Exam.objects.get(id=pk)
        questions = list(exam.questions.all())
        question_ids = [q.id for q in questions]
        problems = Problem.objects.filter(question__in=question_ids)
        problem_ids = [p.id for p in problems]
        expected_problem_attachments = []
        expected_nodes = set()
        for p in problems:
            pas = list(ProblemAttachment.objects.filter(source=p.id).values())
            for pa in pas:
                # maybe a question could be in multiple tests, hence this check
                if pa["target_id"] in problem_ids:
                    expected_nodes.add(str(pa["source_id"]))
                    expected_nodes.add(str(pa["target_id"]))
                    expected_problem_attachments.append((pa["source_id"], pa["target_id"]))
        actual_problem_attachments = []
        actual_nodes = set()
        for p in problems:
            apas = list(ActualProblemAttachment.objects.filter(source=p.id).values())
            for apa in apas:
                # maybe a question could be in multiple tests, hence this check
                if apa["target_id"] in problem_ids:
                    actual_nodes.add(str(apa["source_id"]))
                    actual_nodes.add(str(apa["target_id"]))
                    actual_problem_attachments.append((apa["source_id"], apa["target_id"]))

        expected_ks = nx.Graph()
        expected_ks.add_nodes_from(list(expected_nodes))
        expected_ks.add_edges_from(expected_problem_attachments)

        actual_ks = nx.Graph()
        actual_ks.add_nodes_from(list(actual_nodes))
        actual_ks.add_edges_from(actual_problem_attachments)

        print(f"Expected problem attachments: {expected_problem_attachments}")
        print(f"Actual problem attachments: {actual_problem_attachments}")
        # leven_dist = levenshtein_distance(str(expected_problem_attachments), str(actual_problem_attachments))
        # print(f"Distance: {leven_dist}")
        ged = nx.algorithms.similarity.graph_edit_distance(expected_ks, actual_ks)
        print(f"Graph edit distance = {ged}")
        diff_edges = set(expected_problem_attachments).symmetric_difference(set(actual_problem_attachments))

        for edge in diff_edges:
            source_problem = Problem.objects.get(pk=edge[0])
            target_problem = Problem.objects.get(pk=edge[1])
            DiffProblemAttachment.objects.get_or_create(source=source_problem,
                                                        target=target_problem)
        GraphEditDistance.objects.update_or_create(exam=exam, ged=ged)
        return Response({"ged": ged}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='submitExam', url_name='submitExam', permission_classes=[IsStudentUser])
    def submit_exam(self, request, pk):
        '''
            Submits exam answers that student had.
        '''
        choices_ids = request.data.get('choices')
        question_ids = Choice.objects.filter(
            pk__in=choices_ids, correct_answer=False).values_list('question', flat=True)
        wrong_question_ids = Choice.objects.filter(
            question__in=question_ids, correct_answer=False).values_list('question', flat=True)

        print(f"Question ids {question_ids}")
        print(f"Choices ids {choices_ids}")
        correct_questions = Question.objects.filter(exam=pk).exclude(id__in=wrong_question_ids)
        print(f"Wrong question ids {wrong_question_ids}")
        print(f"Correct question ids {correct_questions}")

        correct_choices = Choice.objects.filter(question__in=correct_questions, correct_answer=True)
        correct_choices_ids = [c_c.id for c_c in correct_choices]

        states_likelihoods = request.data["states_likelihoods"]
        exam = Exam.objects.get(id=request.data["id"])
        answered_questions = request.data["answered_questions"]
        all_questions = list(exam.questions.all())
        all_questions_ids = [q.id for q in all_questions]
        question_idx = all_questions_ids.index(answered_questions[-1]["id"])
        # sorting necessary so that current state and response pattern are correct
        answered_questions.sort(key=lambda q: q['id'])
        print(f"states_likelihoods before update {states_likelihoods}")
        latest_answer_correct = Choice.objects.get(id=choices_ids[-1]).correct_answer
        r = 1 if latest_answer_correct else 0
        ret_val = update_likelihoods_markov(question_idx, states_likelihoods, r)
        terminate_test = False
        if ret_val == 'terminate test':
            terminate_test = True
        else:
            states_likelihoods = ret_val
        # select state with highest likelihood
        current_state = max(states_likelihoods, key=lambda key: states_likelihoods[key])
        response_pattern = ["0" for _ in range(len(all_questions))]
        chces = sorted(choices_ids)
        for i in range(len(answered_questions)):
            for chc in answered_questions[i]["choices"]:
                if chc["id"] in choices_ids and chc["id"] in correct_choices_ids:
                    response_pattern[i] = "1"
        response_pattern = "".join(response_pattern)
        print(f"Response pattern {response_pattern}")
        score = correct_choices.count()
        print(f"Score {score}/{len(answered_questions)}")
        serializer = self.get_serializer(data={
            'exam': self.get_object().id,
            'user': request.user.id,
            'score': score,
            'choices': choices_ids,
            'response_pattern': response_pattern,
            'state': current_state
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        maximum_score = Choice.objects.filter(correct_answer=True, question__exam=pk).count()

        if maximum_score / 2 < score:
            self.request.user.passed_exams.add(self.get_object())

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='submitQuestion', url_name='submitQuestion',
            permission_classes=[IsStudentUser])
    def submit_question(self, request, pk):
        exam = Exam.objects.get(id=request.data["id"])
        all_questions = list(exam.questions.all())
        all_questions_ids = [q.id for q in all_questions]
        answered_questions = request.data['answered_questions']
        question_idx = all_questions_ids.index(answered_questions[-1]["id"])
        # sorting necessary so that current state and response pattern are correct
        answered_questions.sort(key=lambda q: q['id'])
        choices = request.data['choices']
        states_likelihoods = request.data['states_likelihoods']
        print(f"Choices ids {choices}")
        print(f"states_likelihoods before update {states_likelihoods}")
        latest_answer_correct = Choice.objects.get(id=choices[-1]).correct_answer
        r = 1 if latest_answer_correct else 0
        ret_val = update_likelihoods_markov(question_idx, states_likelihoods, r)
        terminate_test = False
        if ret_val == 'terminate test':
            terminate_test = True
        else:
            states_likelihoods = ret_val
        next_question, _ = determine_next_question(answered_questions,
                                                   choices, pk, states_likelihoods)
        return Response({"next_question": QuestionSerializer(next_question).data, "states_likelihoods": states_likelihoods,
                         "terminate_test": terminate_test},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='getXML')
    def getXML(self, request, pk):
        '''
            Fetches XML file generated using IMS QTA specs.
        '''
        file = File(open(f'./static/{pk}.xml', 'r'))
        data = file.read()
        return Response(data)

    @action(detail=True, methods=['get'], url_path='personalizedQuestionsOrder')
    def get_personalized_questions_order(self, request, pk):
        questions = self.get_object().questions.all()

        key = order_questions_actual if self.get_object().mode == 'actual' else order_questions_expected
        questions = sorted(questions, key=key)
        return Response(QuestionSerializer(questions, many=True).data)

    @action(detail=True, methods=['get'], url_path='getStatesLikelihoods', url_name='getStatesLikelihoods')
    def get_states_likelihoods(self, request, pk):
        """Gets called once every time an exam is taken,
        before the first question is loaded
        """
        exam = Exam.objects.get(id=pk)
        all_questions = list(exam.questions.all())
        all_questions_ids = [q.id for q in all_questions]
        all_problems = list(Problem.objects.filter(question__in=all_questions_ids))
        len_problems = len(all_problems)
        start_problem = all_problems[0]
        state_matrix = []
        state_matrix.append("0" * len_problems)
        state_matrix.append("1" + "0" * (len_problems - 1))
        curr_lst = ["0" for i in range(len_problems)]
        curr_lst[0] = "1"

        print(f"Exam mode {exam.mode}")
        is_actual = True
        if exam.mode == 'expected':
            is_actual = False

        # 1. generate knowledge states
        state_matrix = generate_knowledge_states(all_problems, start_problem, state_matrix,
                                                 len_problems, curr_lst, set(), is_actual)
        num_states = len(state_matrix)
        states_likelihoods = {}
        for state in state_matrix:
            states_likelihoods[state] = round(1/num_states, 2)
        print(f"states_likelihoods initial {states_likelihoods}")

        # 2. set response patterns
        response_patterns = {state: 0 for state in state_matrix}
        exam_results = ExamResult.objects.filter(exam=pk)

        for e_r in exam_results:
            res_pat = e_r.response_pattern
            response_patterns[res_pat] = response_patterns[res_pat] + 1 if res_pat in response_patterns else 1
        # num_response_patterns = sum(response_patterns.values())
        # # 3. response pattern-based update
        # states_likelihoods = update_likelihoods_per_response_patterns(state_matrix, response_patterns,
        #                                                               num_response_patterns)
        # print(f"states_likelihoods after update based on response patterns {states_likelihoods}")
        # # 4. state frequency-based update
        # states_likelihoods = update_likelihoods_per_number_of_students_in_state(states_likelihoods,
        #                                                                         exam_results)
        # print(f"states_likelihoods after update based on number of students per state {states_likelihoods}")
        return Response(states_likelihoods, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='getEasiestQuestion', url_name='getEasiestQuestion')
    def get_easiest_question(self, request, pk):
        exam = Exam.objects.get(id=pk)
        questions = list(exam.questions.all())
        questions.sort(key=lambda el: el.num_correct_answers)
        return Response(QuestionSerializer(questions[-1]).data)

    @action(detail=True, methods=['get'], url_path='getCurrentKnowledgeState',
            url_name='getCurrentKnowledgeState', permission_classes=[IsAuthenticated])
    def get_current_knowledge_state(self, request, pk):
        current_state = ExamResult.objects.filter(exam=self.get_object(), user=self.request.user).order_by('pk').values().last()
        exam = Exam.objects.get(id=pk)
        all_questions = list(exam.questions.all())
        all_questions_ids = [q.id for q in all_questions]
        all_problems = list(Problem.objects.filter(question__in=all_questions_ids))
        len_problems = len(all_problems)
        start_problem = all_problems[0]
        state_matrix = []
        state_matrix.append("0" * len_problems)
        state_matrix.append("1" + "0" * (len_problems - 1))
        curr_lst = ["0" for i in range(len_problems)]
        curr_lst[0] = "1"

        print(f"Exam mode {exam.mode}")
        is_actual = True
        if exam.mode == 'expected':
            is_actual = False

        state_matrix = generate_knowledge_states(all_problems, start_problem, state_matrix,
                                                 len_problems, curr_lst, set(), is_actual)

        def map_state_matrix_edges(element):
            def get_edges(el):
                edges = set()
                if '1' not in el:
                    state_matrix_without_zeros = [state for state in state_matrix if '1' in state]
                    min_ones = min(state_matrix_without_zeros, key=lambda x: x.count('1'))
                    return filter(lambda x: x.count('1') == min_ones.count('1'), state_matrix)
                for state in state_matrix:
                    if state == el:
                        continue
                    for tid, tar_problem in enumerate(state):
                        if tar_problem != '1':
                            continue

                        for sid, src_problem in enumerate(el):
                            if src_problem != '1':
                                continue
                            if is_actual and ActualProblemAttachment.objects.filter(source=all_problems[sid].id,
                                                                                    target=all_problems[tid].id).exists():
                                edges.add(state)
                            if not is_actual and ProblemAttachment.objects.filter(source=all_problems[sid].id,
                                                                                  target=all_problems[tid].id).exists():
                                edges.add(state)
                return edges
            return {
                'code': element,
                'edges': get_edges(element)
            }

        new_state_matrix = map(map_state_matrix_edges, state_matrix)
        return Response({"current_state": current_state['state'], "states": new_state_matrix}, status=status.HTTP_200_OK)


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

    def get_permissions(self):
        if self.action == 'destroy':
            self.permission_classes = [IsTeacherUser]
        else:
            self.permission_classes = [IsAuthenticated]

        return super(DomainViewSet, self).get_permissions()

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
        '''
            Returns personalized exams that can be taken next.
        '''
        if self.request.user.is_teacher:
            return Response(ExamSerializer(
                Exam.objects.filter(subject__teacher=self.request.user, subject=self.get_object().subject), many=True).data)

        nodes_to_check = list(self.queryset.get(pk=pk).problems.filter(source_problems__isnull=True))
        nodes_to_return = []

        while len(nodes_to_check):
            current_node = nodes_to_check.pop()
            exam_id = current_node.question.exam.id if current_node.question and current_node.question.exam else None
            if self.request.user.passed_exams.filter(pk=exam_id).exists():
                nodes_to_check += Problem.objects.filter(
                    pk__in=current_node.target_problems.all().values_list('target'))
            else:
                if current_node.question and current_node.question.exam and current_node.question.exam not in nodes_to_return:
                    nodes_to_return.append(current_node.question.exam)

        return Response(ExamSerializer(nodes_to_return, many=True).data)

    @action(detail=True, methods=['patch'], url_path='add-student')
    def add_student(self, request, pk):
        '''
            Adds a student to domain (and subject).
        '''
        self.get_object().subject.students.add(User.objects.get(pk=request.data.get('id')))
        return HttpResponse('')


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

        if not is_cyclic(nodes):
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
        'default': ProblemSerializer
    }
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


class GraphEditDistanceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GraphEditDistance.objects.all()
    serializers = {
        'default': GraphEditDistanceSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @action(detail=True, methods=['get'], url_path='getByExamId')
    def getByExamId(self, request, pk):
        exam = Exam.objects.get(pk=pk)
        return Response(exam.ged.all()[0].ged, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='getByDomainId')
    def getByDomainId(self, request, pk):
        domain = Domain.objects.get(pk=pk)
        subject = domain.subject
        exams = list(subject.exams.all())
        ged = 0
        for exam in exams:
            if not exam.ged.count() > 0:
                continue
            ged += exam.ged.all()[0].ged

        return Response(ged, status=status.HTTP_200_OK)
