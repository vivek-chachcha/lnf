# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0009_auto_20151031_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=200, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(upload_to='posts', blank=True, null=True),
        ),
    ]
