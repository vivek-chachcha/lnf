# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=200)),
                ('breed', models.CharField(max_length=200)),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('sex', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
        ),
    ]
