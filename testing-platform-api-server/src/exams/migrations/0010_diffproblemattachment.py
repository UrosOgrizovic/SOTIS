# Generated by Django 3.0.8 on 2021-01-05 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0009_auto_20201229_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiffProblemAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diff_target_problems', to='exams.Problem')),
                ('target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diff_source_problems', to='exams.Problem')),
            ],
        ),
    ]
