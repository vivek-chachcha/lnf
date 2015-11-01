# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LNF', '0011_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.FloatField(null=True)),
                ('long', models.FloatField(null=True)),
                ('name', models.CharField(max_length=30)),
                ('breed', models.CharField(max_length=30)),
                ('colour', models.CharField(max_length=30)),
                ('description', models.CharField(null=True, blank=True, max_length=200)),
                ('date_created', models.DateTimeField(verbose_name='date posted')),
                ('date', models.DateTimeField(verbose_name='date lost/found')),
                ('modified_date', models.DateTimeField(verbose_name='date last modified')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, default='M')),
                ('picture', models.ImageField(null=True, blank=True, upload_to='posts')),
                ('state', models.CharField(choices=[('0', 'Lost'), ('1', 'Found')], max_length=1, default='0')),
            ],
        ),
    ]
