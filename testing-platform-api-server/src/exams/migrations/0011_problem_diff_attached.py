# Generated by Django 3.0.8 on 2021-01-05 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0010_diffproblemattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='diff_attached',
            field=models.ManyToManyField(blank=True, related_name='_problem_diff_attached_+', through='exams.DiffProblemAttachment', to='exams.Problem'),
        ),
    ]
