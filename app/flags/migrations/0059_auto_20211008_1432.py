# Generated by Django 3.1.8 on 2021-10-08 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0058_auto_20211008_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colorgroup',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='flagelement',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='mainflag',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
