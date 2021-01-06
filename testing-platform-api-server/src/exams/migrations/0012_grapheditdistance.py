# Generated by Django 3.0.8 on 2021-01-06 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0011_problem_diff_attached'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraphEditDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ged', models.IntegerField(default=0)),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ged', to='exams.Exam')),
            ],
        ),
    ]
