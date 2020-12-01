from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from src.exams.models import Exam, Question, Choice
from src.exams.serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer, ExamChoiceSerializer

import json
import uuid

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
        return self.serializers.get(self.action, self.serializers['default'])

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='submitExam', url_name='submitExam')
    # def submit_exam(self):
    def submit_exam(self, instance):
        try:
            json_exam_choice = json.loads(self.request.body)
            exam_choice = {'id': uuid.UUID(json_exam_choice['id']),
                           'choices': [uuid.UUID(choice) for choice in json_exam_choice['choices']],
                           'score': 0}

            exam = Exam.objects.filter(id=exam_choice['id'])[0]
            questions = exam.questions.all()
            choices_by_question = [question.choices.all() for question in questions]
            # choices = [choice for choice in choices if choice in exam_choice['choices']]
            for i in range(len(choices_by_question)):
                for j in range(len(choices_by_question[i])):
                    if choices_by_question[i][j].id in exam_choice['choices'] and \
                            choices_by_question[i][j].correct_answer:
                        exam_choice['score'] += 1

            return Response(ExamChoiceSerializer(exam_choice).data,
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Wrong auth token' + e}, status=status.HTTP_400_BAD_REQUEST)


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
