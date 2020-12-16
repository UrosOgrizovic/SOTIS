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


class CreateQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        print(choices)
        for choice in choices:
            serializer = ChoiceSerializer(data=choice)
            serializer.is_valid(raise_exception=True)
            question.choices.add(serializer.save())

        return question

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'exam', 'choices']
        depth = 1


class ProblemAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemAttachment
        exclude = ()


class ProblemSerializer(serializers.ModelSerializer):
    """ read_only=True because create() doesn't support writable nested fields by default
    (used in ProblemViewSet -> custom_make)"""
    source_problems = ProblemAttachmentSerializer(many=True, read_only=True)
    target_problems = ProblemAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        exclude = ()


class CreateExamSerializer(serializers.ModelSerializer):
    questions = CreateQuestionSerializer(many=True)

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        exam = Exam.objects.create(**validated_data)
        for question in questions:
            serializer = CreateQuestionSerializer(data=question)
            serializer.is_valid(raise_exception=True)
            exam.questions.add(serializer.save())

        return exam

    class Meta:
        model = Exam
        exclude = ()

class DomainSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many=False)
    problems = ProblemSerializer(many=True)

    class Meta:
        model = Domain
        exclude = ()
