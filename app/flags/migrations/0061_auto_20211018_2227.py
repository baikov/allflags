# Generated by Django 3.1.8 on 2021-10-18 19:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0060_metatemplate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainflag',
            name='short_description',
        ),
        migrations.AddField(
            model_name='historicalflagpicture',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalflagpicture',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Published'),
        ),
        migrations.AddField(
            model_name='historicalflagpicture',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
