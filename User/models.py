# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
__author__ = 'HeYang'


from django.db import models


class CMDBUser(models.Model):
    # 用户表
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")
    phone = models.CharField(max_length=32, verbose_name="电话")
    photo = models.ImageField(upload_to="images", verbose_name="照片")
    # ImageFied必须安装pil或者pillow的基础上使用

    def __unicode__(self):
        return self.username


class Permission(models.Model):
    # 权限表
    name = models.CharField(max_length=32, verbose_name="权限名称")
    obj_id = models.IntegerField(verbose_name="操作对象")
    description = models.TextField(verbose_name="权限描述")

    def __unicode__(self):
        return self.name


class Group(models.Model):
    # 用户组表
    name = models.CharField(max_length=32, verbose_name="组名称")

    def __unicode__(self):
        return self.name


class User_Group(models.Model):
    # 用户和组的关系表(第三张表)
    user_id = models.ForeignKey("CMDBUser", verbose_name="用户id")
    group_id = models.ForeignKey("Group", verbose_name="组id")


class User_Permission(models.Model):
    # 用户和权限的关系表(第三张表)
    user_id = models.ForeignKey("CMDBUser", verbose_name="用户id")
    permission_id = models.ForeignKey("Permission", verbose_name="权限id")


class Group_Permission(models.Model):
    # 用户组和权限的关系表(第三张表)
    group_id = models.ForeignKey("Group", verbose_name="组id")
    permission_id = models.ForeignKey("Permission", verbose_name="权限id")






