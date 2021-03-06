# Generated by Django 3.1.8 on 2021-06-29 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0008_flagelement'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorgroup',
            name='en_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Name (en)'),
        ),
        migrations.AlterField(
            model_name='colorgroup',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name (ru)'),
        ),
        migrations.AlterField(
            model_name='colorgroup',
            name='short_name',
            field=models.CharField(max_length=50, verbose_name='Short name'),
        ),
        migrations.CreateModel(
            name='MainFlag',
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
                ('title', models.CharField(blank=True, max_length=250, verbose_name='Title')),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='Flag name')),
                ('adopted_date', models.DateField(blank=True, null=True, verbose_name='Adopted date')),
                ('proportion', models.CharField(blank=True, max_length=10, verbose_name='??????????????????')),
                ('short_description', models.TextField(blank=True, max_length=550, verbose_name='Short description')),
                ('flag_day', models.DateField(blank=True, null=True, verbose_name='Flag day')),
                ('construction_image', models.ImageField(blank=True, upload_to='', verbose_name='Construction image')),
                ('design_description', models.TextField(blank=True, verbose_name='Design description')),
                ('history_text', models.TextField(blank=True, verbose_name='Flag history')),
                ('colors', models.ManyToManyField(blank=True, related_name='flags', to='flags.Color', verbose_name='Colors')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='flags.country', verbose_name='Country')),
                ('elements', models.ManyToManyField(blank=True, related_name='flags_with_elem', to='flags.FlagElement', verbose_name='Flags elements')),
            ],
            options={
                'verbose_name': 'Country flag',
                'verbose_name_plural': 'Country flags',
            },
        ),
    ]
