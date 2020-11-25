# Generated by Django 3.0.8 on 2020-11-25 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('choice_text', models.CharField(max_length=200, unique=True, verbose_name='ChoiceText')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_text', models.CharField(max_length=255, unique=True, verbose_name='QuestionText')),
                ('correct_answer', models.CharField(max_length=200, verbose_name='CorrectAnswer')),
                ('choices', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Choice')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('questions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Question')),
            ],
        ),
    ]