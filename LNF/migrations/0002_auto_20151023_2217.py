# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20151012220059 on 2015-10-24 05:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='description_test',
            new_name='description_text',
        ),
    ]
