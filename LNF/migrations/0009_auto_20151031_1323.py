# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0008_auto_20151027_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(blank=True, upload_to='posts'),
        ),
    ]
