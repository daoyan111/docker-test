# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=32, verbose_name='\u503c')),
                ('type', models.CharField(max_length=32, verbose_name='token\u7c7b\u578b')),
                ('time', models.DateTimeField(verbose_name='\u6ce8\u518c\u65f6\u95f4')),
            ],
        ),
    ]
