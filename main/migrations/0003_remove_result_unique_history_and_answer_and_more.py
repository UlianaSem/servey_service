# Generated by Django 5.0.1 on 2024-02-09 14:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='result',
            name='Unique history and answer',
        ),
        migrations.AddField(
            model_name='result',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
