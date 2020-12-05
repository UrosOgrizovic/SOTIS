from rest_framework import serializers

from src.exams.models import Choice, Question, Exam, ExamResult, Domain, Subject
from src.users.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ()


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'question']  # don't serialize correct_answer, so that no cheating can occur
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'exam', 'choices']
        depth = 1


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    subject = SubjectSerializer(many=False)
    creator = UserSerializer(many=False)

    class Meta:
        model = Exam
        exclude = ('completed_by',)
        depth = 2


class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = ['id', 'score']

class DomainSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many=False)

    class Meta:
        model = Domain
        exclude = ()
