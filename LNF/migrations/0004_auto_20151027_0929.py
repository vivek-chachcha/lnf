# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2015-10-27 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0003_post_pet_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('0', 'lost'), ('1', 'found')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='pet_picture',
            field=models.ImageField(default='/static/LNF/images/chinesecrested.jpg', upload_to='/static/LNF/images/'),
        ),
    ]
