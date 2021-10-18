# Generated by Django 3.1.8 on 2021-10-17 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0059_auto_20211008_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(choices=[('MainFlag', 'MainFlag'), ('Region', 'Region'), ('Country', 'Country'), ('ColorGroup', 'ColorGroup'), ('FlagElement', 'FlagElement')], default='MainFlag', max_length=50, verbose_name='Model')),
                ('tag', models.CharField(choices=[('title', 'Title'), ('descr', 'Description')], default='title', max_length=50, verbose_name='Meta-tag')),
                ('template', models.TextField(blank=True, max_length=400, verbose_name='Template')),
            ],
            options={
                'verbose_name': 'Meta template',
                'verbose_name_plural': 'Meta templates',
            },
        ),
    ]
