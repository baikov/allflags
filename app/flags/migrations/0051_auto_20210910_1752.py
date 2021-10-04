# Generated by Django 3.1.8 on 2021-09-10 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0050_remove_mainflag_colors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ('ordering',), 'verbose_name': 'Color', 'verbose_name_plural': 'Flag colors'},
        ),
        migrations.AlterModelOptions(
            name='colorgroup',
            options={'ordering': ('ordering',), 'verbose_name': 'Color group', 'verbose_name_plural': 'Color groups'},
        ),
        migrations.AlterModelOptions(
            name='flagelement',
            options={'ordering': ('ordering',), 'verbose_name': 'Flag element', 'verbose_name_plural': 'Flags elements'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('ordering',), 'verbose_name': 'Region', 'verbose_name_plural': 'Regions'},
        ),
        migrations.RemoveField(
            model_name='country',
            name='ordering',
        ),
        migrations.RemoveField(
            model_name='mainflag',
            name='ordering',
        ),
        migrations.AddField(
            model_name='flagfact',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Published'),
        ),
        migrations.AddField(
            model_name='historicalflag',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Published'),
        ),
        migrations.AlterField(
            model_name='color',
            name='ordering',
            field=models.PositiveSmallIntegerField(db_index=True, default=500, verbose_name='Ordering'),
        ),
        migrations.AlterField(
            model_name='colorgroup',
            name='ordering',
            field=models.PositiveSmallIntegerField(db_index=True, default=500, verbose_name='Ordering'),
        ),
        migrations.AlterField(
            model_name='flagelement',
            name='ordering',
            field=models.PositiveSmallIntegerField(db_index=True, default=500, verbose_name='Ordering'),
        ),
        migrations.AlterField(
            model_name='flagfact',
            name='ordering',
            field=models.PositiveSmallIntegerField(db_index=True, default=10, verbose_name='Ordering'),
        ),
        migrations.AlterField(
            model_name='historicalflag',
            name='ordering',
            field=models.PositiveSmallIntegerField(db_index=True, default=500, verbose_name='Ordering'),
        ),
        migrations.AlterField(
            model_name='region',
            name='ordering',
            field=models.PositiveSmallIntegerField(db_index=True, default=500, verbose_name='Ordering'),
        ),
        migrations.DeleteModel(
            name='FlagEmoji',
        ),
    ]