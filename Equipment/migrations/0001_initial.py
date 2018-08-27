# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=32, verbose_name='\u4e3b\u673a\u540d')),
                ('mac', models.CharField(max_length=32, verbose_name='mac\u5730\u5740')),
                ('ip', models.CharField(max_length=32, verbose_name='IP\u5730\u5740')),
                ('sys_type', models.CharField(max_length=32, verbose_name='\u7cfb\u7edf\u7c7b\u578b')),
                ('cpu_count', models.IntegerField(verbose_name='cpu\u4e2a\u6570')),
                ('disk', models.CharField(max_length=32, verbose_name='\u786c\u76d8')),
                ('memory', models.CharField(max_length=32, verbose_name='\u5185\u5b58')),
                ('sys_version', models.CharField(default=' ', max_length=64, verbose_name='\u7cfb\u7edf\u7248\u672c')),
            ],
        ),
    ]
