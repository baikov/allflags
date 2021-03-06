# Generated by Django 3.1.8 on 2021-08-02 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0025_auto_20210802_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='en_chief_of_state',
            field=models.CharField(blank=True, max_length=900, verbose_name='Chief of state (en)'),
        ),
        migrations.AlterField(
            model_name='country',
            name='en_head_of_government',
            field=models.CharField(blank=True, max_length=900, verbose_name='Head of government (en)'),
        ),
        migrations.AlterField(
            model_name='country',
            name='ru_chief_of_state',
            field=models.CharField(blank=True, max_length=900, verbose_name='Chief of state (ru)'),
        ),
        migrations.AlterField(
            model_name='country',
            name='ru_head_of_government',
            field=models.CharField(blank=True, max_length=900, verbose_name='Head of government (ru)'),
        ),
    ]
