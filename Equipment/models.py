# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
__author__ = 'HeYang'


from django.db import models


class Equipment(models.Model):
    # 设备表
    hostname = models.CharField(max_length=32, verbose_name="主机名")
    mac = models.CharField(max_length=32, verbose_name="mac地址")
    ip = models.CharField(max_length=32, verbose_name="IP地址")
    sys_type = models.CharField(max_length=32, verbose_name="系统类型")
    cpu_count = models.IntegerField(verbose_name="cpu个数")
    disk = models.CharField(max_length=32, verbose_name="硬盘")
    memory = models.CharField(max_length=32, verbose_name="内存")
    sys_version = models.CharField(max_length=64, verbose_name="系统版本", default=' ')

    def __unicode__(self):
        return self.hostname


class ApiToken(models.Model):
    value = models.CharField(max_length=32, verbose_name='值')
    type = models.CharField(max_length=32, verbose_name="token类型")
    time = models.DateTimeField(verbose_name="注册时间")
