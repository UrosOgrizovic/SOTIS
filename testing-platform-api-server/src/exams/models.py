from django.db import models
from django.conf import settings

from django.utils.html import strip_tags

class Subject(models.Model):
    title = models.CharField(max_length=255, null=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subjects', blank=True)

    def __str__(self):
        return f'{self.title}'

class Exam(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams', null=True)
    completed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='passed_exams', blank=True)

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    question_text = models.TextField(blank=True, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', null=True)

    def __str__(self):
        return f'{strip_tags(self.question_text)}'


class Choice(models.Model):
    choice_text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name='choices', null=True)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.choice_text}'


class ExamResult(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='results', null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results', null=True)
    choices = models.ManyToManyField(Choice, related_name='results', blank=True)

    def __str__(self):
        if self.user and self.exam:
            return f'{self.user.username}|{self.exam.title}|{self.score}'
        return 'Exam Choice'


class Domain(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.SET_NULL, related_name='domain', null=True)
    title = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.title}'


class Problem(models.Model):
    exam = models.OneToOneField(Exam, on_delete=models.SET_NULL, related_name='problem', null=True)
    title = models.CharField(max_length=255, null=True)
    attached = models.ManyToManyField('self', related_name='attached_problems', blank=True, through='ProblemAttachment')

    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='problems', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class ProblemAttachment(models.Model):
    source = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='target_problems', null=True, blank=True)
    target = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='source_problems', null=True, blank=True)
