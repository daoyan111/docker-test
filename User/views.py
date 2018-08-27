# _*_ coding: utf-8 _*_
__author__ = 'HeYang'

from django.shortcuts import render, redirect
from django.http import JsonResponse

from User.forms import RegisterForm, LoginForm
from NB_CMDB.views import valid_phone, getmd5, loginValid
from User.models import CMDBUser

from PIL import Image

# Create your views here.


def logout(request):
    del request.session["username"]
    del request.session["isLogin"]
    return redirect("/login")


@loginValid
def index(request):
    register = RegisterForm()

    return render(request, "index.html", locals())


def login(request):
    is_error = 0
    msg = "账号或密码错误，请重新输入"
    if request.method == "POST":
        login = LoginForm(request.POST)
        if login.is_valid():
            phone = request.POST["phone"]
            password = request.POST["password"]
            try:
                user = CMDBUser.objects.get(phone=phone)
            except:
                is_error = 1
                return render(request, "login.html", locals())
            else:
                md5_password = getmd5(password)
                if user.password == md5_password:
                    response = redirect("/index")
                    response.set_cookie("username", user.username)
                    request.session["username"] = user.username
                    request.session["isLogin"] = True
                    return response
                else:
                    is_error = 1
                    return render(request, "login.html", locals())
        else:
            msg = "密码或账号未填写"
            return render(request, "login.html", locals())
    else:
        login = LoginForm()
        return render(request, "login.html", locals())


def phone_valid(request):
    res = {"type": "error", "data": ""}
    if request.method == "GET":
        phone = request.GET["phone"]
        result = valid_phone(phone)
        if phone == result:
            res["type"] = "success"
        else:
            res["data"] = result
    else:
        res["data"] = "请输入手机号"
    return JsonResponse(res)


def register(request):
    res = {"type": "error", "data": ""}
    if request.method == "POST":
        reg = RegisterForm(request.POST, request.FILES)
        if reg.is_valid():
            # 验证通过的字典形式的数据
            cleand_data = reg.cleaned_data
            username = cleand_data["username"]
            password = cleand_data["password"]
            email = cleand_data["email"]
            phone = cleand_data["phone"]
            photo = cleand_data["photo"]

            user = CMDBUser()
            user.username = username
            # 加密密码
            user.password = getmd5(password)
            user.email = email
            user.phone = phone

            # 保存图片
            name = "static/image/" + phone + '_' + photo.name
            img = Image.open(photo)
            img.save(name)

            # 数据库当中存储图片的路径
            user.photo = "image/" + phone + '_' + photo.name
            user.save()

            res["type"] = "success"
            res["data"] = "success"
        else:
            res["data"] = reg.errors
    else:
        res["data"] = "request error"
    return JsonResponse(res)

