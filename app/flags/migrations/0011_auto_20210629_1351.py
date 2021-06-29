# Generated by Django 3.1.8 on 2021-06-29 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0010_flagemoji'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flagemoji',
            name='flag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emoji', to='flags.mainflag', verbose_name='Emoji'),
        ),
    ]