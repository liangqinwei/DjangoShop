from typing import Tuple

from django.db import models
from datetime import datetime
from django import forms
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.contrib.auth.models import User

# Create your models here.
from users.manager import MyUserManager


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """
    用户信息
    """
    GENDER_CHOICES: Tuple[Tuple[str, str], Tuple[str, str]] = (("male", "男"), ("femal", "女"))

    # 删除字段  这里是不想要的字段，直接赋值为None即可
    first_name = None
    last_name = None
    date_joined = None
    username = models.CharField(verbose_name="姓名", max_length=30, default='', unique=True)
    birthday = models.DateField(verbose_name="出生年月", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", max_length=6, choices=GENDER_CHOICES, default="female")
    mobile = models.CharField(verbose_name="电话", max_length=11)
    email = models.EmailField(verbose_name="邮箱", max_length=100, default='')
    nickname = models.CharField(verbose_name="昵称", max_length=30, default='')
    is_staff = models.IntegerField(verbose_name="是否为员工", default=0)
    is_superuser = models.IntegerField(verbose_name="是否为超管", default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = "admin_user"

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    验证码
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(verbose_name="验证码", max_length=10)
    mobile = models.CharField(verbose_name="电话", max_length=11)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
