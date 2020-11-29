from rest_framework import serializers

from src.exams.models import Choice, Question, Exam


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex')

    class Meta:
        model = Choice
        fields = '__all__'
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex')

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'exam', 'choices']
        depth = 1


class ExamSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex')

    class Meta:
        model = Exam
        fields = ['id', 'title', 'creator', 'questions']
        depth = 1
