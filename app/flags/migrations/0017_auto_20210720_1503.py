# Generated by Django 3.1.8 on 2021-07-20 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0016_auto_20210720_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='countries2', to='flags.newregion'),
        ),
    ]
