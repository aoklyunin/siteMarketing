# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-24 15:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sworks', '0010_auto_20170424_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attemptcomment',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 24, 18, 28, 14, 758543)),
        ),
        migrations.AlterField(
            model_name='mark',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 24, 18, 28, 14, 759544)),
        ),
    ]
