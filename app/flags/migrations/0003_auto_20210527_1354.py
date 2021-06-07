# Generated by Django 3.1.8 on 2021-05-27 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0002_auto_20210527_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='area_global_rank',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Area global rank'),
        ),
        migrations.AlterField(
            model_name='country',
            name='external_debt_global_rank',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='External debt global rank'),
        ),
        migrations.AlterField(
            model_name='country',
            name='gdp_global_rank',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='GDP global rank'),
        ),
        migrations.AlterField(
            model_name='country',
            name='population_global_rank',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Population global rank'),
        ),
    ]