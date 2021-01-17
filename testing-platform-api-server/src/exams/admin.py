from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from django.http import HttpResponse
import csv
from src.exams.models import Exam, Choice, Question, Subject, Domain, Problem, ProblemAttachment


def export_to_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response


export_to_csv.short_description = 'Export to CSV'  # short description


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
    actions = [export_to_csv]

@admin.register(Question)
class QuestionAdmin(SummernoteModelAdmin):
    inlines = (ChoiceInline,)

    search_fields = ('question_text',)
    list_display = ('question_text', 'exam')

    summernote_fields = ('question_text',)
    actions = [export_to_csv]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    search_fields = ('choice_text',)
    list_display = ('choice_text', 'question')
    actions = [export_to_csv]


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
    pass
