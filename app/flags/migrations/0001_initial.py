# Generated by Django 3.1.8 on 2021-05-20 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ru_name', models.CharField(blank=True, max_length=250, verbose_name='Currency name (ru)')),
                ('en_name', models.CharField(blank=True, max_length=250, verbose_name='Currency name (en)')),
                ('iso_num', models.CharField(blank=True, max_length=250, verbose_name='Numeric code ISO 4217')),
                ('iso_code', models.CharField(blank=True, max_length=250, verbose_name='Code ISO 4217')),
                ('symbol', models.CharField(blank=True, max_length=5, verbose_name='Symbol')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='Region',
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
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
        ),
        migrations.CreateModel(
            name='Subregion',
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
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subregion', to='flags.region')),
            ],
            options={
                'verbose_name': 'Subregion',
                'verbose_name_plural': 'Subregions',
            },
        ),
    ]
