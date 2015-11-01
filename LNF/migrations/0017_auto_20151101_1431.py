# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0016_auto_20151101_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='breed',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='colour',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='date lost/found'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(null=True, verbose_name='date posted'),
        ),
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
