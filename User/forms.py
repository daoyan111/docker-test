# _*_ coding: utf-8 _*_
__author__ = 'HeYang'

from django import forms
from django.forms import ValidationError

from NB_CMDB.views import valid_phone, valid_password, valid_email


class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "电话"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "密码"}
        )
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=32,
        min_length=6,
        label='用户名',
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "用户名"}
        )
    )
    password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "密码"}
        )
    )
    email = forms.CharField(
        max_length=32,
        min_length=6,
        label="邮箱",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "邮箱"}
        )
    )
    phone = forms.CharField(
        max_length=32,
        min_length=11,
        label="电话",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "电话"}
        )
    )
    photo = forms.ImageField(label="用户头像")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        result = valid_phone(phone)
        if phone == result:
            return phone
        else:
            raise ValidationError(result)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        result = valid_password(password)
        if password == result:
            return password
        else:
            raise ValidationError(result)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        result = valid_email(email)
        if email == result:
            return email
        else:
            raise ValidationError(result)

    def clean(self):
        pass






