from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from src.exams.models import Exam, Question, Choice
from src.exams.serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer


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

    permission_classes = [AllowAny]

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

    permission_classes = [AllowAny]


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

    permission_classes = [AllowAny]