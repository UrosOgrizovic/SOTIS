# Generated by Django 3.0.8 on 2020-12-05 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0006_auto_20201205_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemattachment',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_problems', to='exams.Problem'),
        ),
        migrations.AlterField(
            model_name='problemattachment',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_problems', to='exams.Problem'),
        ),
    ]
