from django.db import models

import uuid

from src.users.models import User

CHOICE_MAX_LEN = 200


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # questions = models.ManyToManyField(Question, related_name='exams')


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField('QuestionText', max_length=255, unique=True)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, related_name='questions', null=True)
    # choices = models.ManyToManyField(Choice, related_name='questions')
    # correct_answer = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='CorrectAnswer', null=True,
    #                                    choices=choices)
    # correct_answers = models.ManyToManyField(Choice, related_name='CorrectAnswers', choices=choices)
    # correct_answer = models.CharField('CorrectAnswer', max_length=CHOICE_MAX_LEN)


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice_text = models.CharField('ChoiceText', max_length=CHOICE_MAX_LEN, unique=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name='choices', null=True)
    correct_answer = models.BooleanField(name='correct_answer', default=False)
