# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0017_auto_20151101_1431'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('name', 'breed', 'colour', 'description', 'sex', 'state', 'date')]),
        ),
    ]
