# Generated by Django 3.0.8 on 2021-01-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0013_question_num_correct_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='examresult',
            name='response_pattern',
            field=models.CharField(default='', max_length=255),
        ),
    ]
