# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userid', models.IntegerField(primary_key=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Salary_type',
            fields=[
                ('salary_typeid', models.IntegerField(primary_key=True)),
                ('typename', models.CharField(max_length=30)),
                ('hour_pay', models.FloatField()),
                ('plus_pay', models.FloatField()),
                ('base_pay', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('peopleid', models.IntegerField(primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('nation', models.CharField(max_length=7)),
                ('sex', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=50)),
                ('birthday', models.DateField()),
                ('date', models.DateField()),
                ('allsalary', models.FloatField(default=0)),
                ('ptype', models.ForeignKey(to='app.Salary_type')),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('salaryid', models.ForeignKey(to='app.People',primary_key=True)),
                ('hour', models.FloatField()),
                ('plus', models.FloatField()),
                ('sub', models.FloatField()),
            ],
        ),


        migrations.CreateModel(
            name='Yewu',
            fields=[
                ('yewuid', models.IntegerField(primary_key=True)),
                ('yewupeopleid', models.ForeignKey(to='app.People')),
                ('title', models.CharField(max_length=50)),
                ('money', models.FloatField()),
                ('person', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('checkinDate', models.DateField()),
                ('beizhu', models.CharField(max_length=100)),
                ('ispermiss', models.BooleanField(default=False)),
                ('isover', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('cardid', models.ForeignKey(to='app.People',primary_key=True)),
                ('start', models.IntegerField()),
                ('over', models.IntegerField()),
                ('date', models.DateField()),
                ('hours', models.IntegerField(default=0)),
            ],
        ),
    ]
