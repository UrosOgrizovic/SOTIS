from __future__ import absolute_import

import os
import sys

from celery import Celery
from celery import task

TESTING = sys.argv[1:2] == ['test']
if not TESTING:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.local")

app = Celery('src.config')

app.config_from_object('django.conf:settings')

# tasks can be added below
@task(name='GenerateIITA')
def generate_iita(correct_answers_matrix, examId):
    import numpy as np

    from learning_spaces.kst.iita import iita

    from src.exams.models import Exam, ActualProblemAttachment

    ks = iita(np.array([np.array(questions_array) for questions_array in correct_answers_matrix]), 1)

    implications = ks.get('implications', [])
    for source_id, target_id in implications:
        question_source = Exam.objects.get(pk=examId).questions.all().order_by('id')[source_id]
        question_target = Exam.objects.get(pk=examId).questions.all().order_by('id')[target_id]

        ActualProblemAttachment.objects.get_or_create(source=question_source.problem,
                                                      target=question_target.problem)
