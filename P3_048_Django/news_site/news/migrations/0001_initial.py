# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-12-27 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=70)),
                ('text', models.TextField(verbose_name='Commenttext')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField()),
                ('text', models.TextField(verbose_name='Text')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Report'),
        ),
    ]
