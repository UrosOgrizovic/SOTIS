# Generated by Django 3.0.8 on 2021-01-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0012_grapheditdistance'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='num_correct_answers',
            field=models.IntegerField(default=0),
        ),
    ]