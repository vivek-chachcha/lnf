# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0002_auto_20151027_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lnf_user',
            name='user',
        ),
        migrations.DeleteModel(
            name='LNF_User',
        ),
    ]
