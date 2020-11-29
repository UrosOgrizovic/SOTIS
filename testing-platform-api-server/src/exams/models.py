from django.db import models

import uuid

from src.users.models import User

CHOICE_MAX_LEN = 200


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('ExamTitle', max_length=255, null=True)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField('QuestionText', max_length=255, unique=True)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, related_name='questions', null=True)


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice_text = models.CharField('ChoiceText', max_length=CHOICE_MAX_LEN, unique=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name='choices', null=True)
    correct_answer = models.BooleanField(name='correct_answer', default=False)
