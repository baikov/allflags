# Generated by Django 3.1.8 on 2021-08-16 14:09

import app.flags.services
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0030_auto_20210809_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='color_meaning',
        ),
        migrations.AddField(
            model_name='color',
            name='flag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='colors_set', to='flags.mainflag', verbose_name='Flag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='color',
            name='order',
            field=models.PositiveSmallIntegerField(default=500, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='historicalflag',
            name='svg_file',
            field=models.FileField(blank=True, upload_to=app.flags.services.historical_flag_img_file_path, verbose_name='SVG image'),
        ),
    ]
