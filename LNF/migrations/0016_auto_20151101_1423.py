# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0015_auto_20151101_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('M/S', 'Male Neutered'), ('F/S', 'Female Spayed'), ('X', 'Unknown')], max_length=1, default='M'),
        ),
    ]
