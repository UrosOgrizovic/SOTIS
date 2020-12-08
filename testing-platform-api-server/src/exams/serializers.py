from rest_framework import serializers

from src.exams.models import Choice, Question, Exam, ExamResult, Domain, Subject, Problem, ProblemAttachment
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


class CreateExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        exclude = ()


class ProblemAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemAttachment
        exclude = ()


class ProblemSerializer(serializers.ModelSerializer):
    source_problems = ProblemAttachmentSerializer(many=True)
    target_problems = ProblemAttachmentSerializer(many=True)

    class Meta:
        model = Problem
        exclude = ()


class DomainSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many=False)
    problems = ProblemSerializer(many=True)

    class Meta:
        model = Domain
        exclude = ()
