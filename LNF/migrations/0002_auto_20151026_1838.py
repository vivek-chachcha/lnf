# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='lon',
            field=models.FloatField(null=True),
        ),
    ]
