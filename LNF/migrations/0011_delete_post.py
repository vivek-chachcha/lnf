# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0010_auto_20151031_1416'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
