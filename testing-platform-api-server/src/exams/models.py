from django.db import models

import uuid

from src.users.models import User

CHOICE_MAX_LEN = 200


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice_text = models.CharField('ChoiceText', max_length=CHOICE_MAX_LEN, unique=True)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField('QuestionText', max_length=255, unique=True)
    choices = models.ForeignKey(Choice, on_delete=models.CASCADE)
    correct_answer = models.CharField('CorrectAnswer', max_length=CHOICE_MAX_LEN)


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)
