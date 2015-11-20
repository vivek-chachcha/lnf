# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkedPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date_bmed', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='BookmarkedPostList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('bmList', models.ManyToManyField(blank=True, to='LNF.BookmarkedPost')),
                ('user', models.OneToOneField(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('lat', models.FloatField(default=None, null=True)),
                ('lon', models.FloatField(default=None, null=True)),
                ('address', models.CharField(default=None, max_length=50, null=True)),
                ('name', models.CharField(max_length=30, null=True)),
                ('breed', models.CharField(max_length=30, null=True)),
                ('colour', models.CharField(max_length=30, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(verbose_name='date posted', null=True)),
                ('date', models.DateField(verbose_name='date lost/found', null=True)),
                ('modified_date', models.DateTimeField(verbose_name='date last modified')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('M/N', 'Male Neutered'), ('F/S', 'Female Spayed'), ('X', 'Unknown')], default='M', max_length=3)),
                ('picture', models.ImageField(blank=True, upload_to='posts', null=True)),
                ('state', models.CharField(choices=[('0', 'Lost'), ('1', 'Found')], default='0', max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='bookmarkedpost',
            name='bmList',
            field=models.ForeignKey(to='LNF.BookmarkedPostList'),
        ),
        migrations.AddField(
            model_name='bookmarkedpost',
            name='post',
            field=models.ForeignKey(to='LNF.Post'),
        ),
    ]
