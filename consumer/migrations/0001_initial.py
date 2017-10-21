# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-19 10:52
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0002_auto_20171019_1052'),
        ('mainApp', '0012_auto_20171019_1052'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vk_link', models.TextField(default='', max_length=10000)),
                ('insta_link', models.TextField(default='', max_length=10000)),
                ('fb_link', models.TextField(default='', max_length=10000)),
                ('balance', models.FloatField(default=0)),
                ('qiwi', models.TextField(default='', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumerTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tc', models.TextField(default='', max_length=100)),
                ('state', models.IntegerField(default=0)),
                ('value', models.FloatField(default=0)),
                ('dt', models.DateTimeField(default=datetime.datetime(2017, 10, 19, 10, 52, 22, 804468))),
                ('comments', models.ManyToManyField(to='mainApp.Comment')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
            ],
        ),
        migrations.CreateModel(
            name='WorkerMarketCamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewCnt', models.IntegerField(default=0)),
                ('link', models.TextField(max_length=1000)),
                ('marketCamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.MarketCamp')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
            ],
        ),
    ]