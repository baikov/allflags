# Generated by Django 3.1.8 on 2021-07-20 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0015_auto_20210708_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('seo_title', models.CharField(blank=True, max_length=250, verbose_name='SEO Title')),
                ('seo_description', models.TextField(blank=True, max_length=400, verbose_name='SEO Description')),
                ('seo_h1', models.CharField(blank=True, max_length=250, verbose_name='SEO H1')),
                ('is_published', models.BooleanField(default=False, verbose_name='Published')),
                ('is_index', models.BooleanField(default=True, verbose_name='index')),
                ('is_follow', models.BooleanField(default=True, verbose_name='follow')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=250, verbose_name='Region name')),
                ('description', models.TextField(blank=True, verbose_name='Region description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subregions', to='flags.newregion', verbose_name='Parent name')),
            ],
            options={
                'verbose_name': 'New Region',
                'verbose_name_plural': 'New Regions',
            },
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='countries', to='flags.newregion'),
        ),
    ]
