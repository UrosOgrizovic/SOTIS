from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin

from src.exams.models import Exam, Choice, Question, Subject, Domain, Problem, ProblemAttachment


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)

    search_fields = ('title',)
    list_display = ('title', 'creator')


@admin.register(Question)
class QuestionAdmin(SummernoteModelAdmin):
    inlines = (ChoiceInline,)

    search_fields = ('question_text',)
    list_display = ('question_text', 'exam')

    summernote_fields = ('question_text',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    search_fields = ('choice_text',)
    list_display = ('choice_text', 'question')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)


@admin.register(ProblemAttachment)
class ProblemAttachment(admin.ModelAdmin):
    pass

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
