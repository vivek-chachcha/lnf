# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0014_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='long',
            new_name='lon',
        ),
    ]
