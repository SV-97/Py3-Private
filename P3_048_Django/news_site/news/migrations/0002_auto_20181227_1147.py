# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-12-27 11:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='titel',
            new_name='title',
        ),
    ]
