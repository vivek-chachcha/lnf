# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2015-10-26 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0002_auto_20151023_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pet_picture',
            field=models.ImageField(default='pet_pics/chinesecrested.jpg', upload_to='pet_pics'),
        ),
    ]
