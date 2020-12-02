from django.db import models
from django.conf import settings

from collections import OrderedDict

class Exam(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    question_text = models.TextField(blank=True, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', null=True)

    def __str__(self):
        return f'{self.question_text}'



class Choice(models.Model):
    choice_text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name='choices', null=True)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.choice_text}'



class ExamChoice(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results', null=True)
