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
        fields = '__all__'
        depth = 1

class ExamSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex')

    class Meta:
        model = Exam
        fields = '__all__'