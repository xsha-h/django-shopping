from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import View

from user.models import UserInfo
from .forms import LoginForm, RegisterForm


# Create your views here.
class LoginView(View):
    """
    和Flask的基于调度方法的类视图一模一样，
    get方法对应前端get请求：
        只是简单的渲染前台登录页面

    post方法对应前端post请求：
        不能通过验证，就返回当前页面
        1、将前端post请求的参数放置在表单中，进行数据合法验证
        2、通过数据合法验证，将获取的参数与数据库数据匹配。django已经提供用户验证，
            从django.contrib.auth中导入authenticate方法
        3、通过用户验证，将user的相关信息保存到session中
        4、以上三步完成最后渲染主页面
    """
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("user", "")
            password = request.POST.get("pwd", "")
            # authenticate验证用户名和密码是否匹配
            user = authenticate(username=username, password=password)
            if user:
                # 将用户的相关信息保存到session中
                login(request, user)
                return redirect(reverse("commodity:index"))
            else:
                return self.get(request)
        else:
            return self.get(request)


class RegisterView(View):
    """
    和Flask的基于调度方法的类视图一模一样，
    get方法对应前端get请求：
        只是简单的渲染前台注册页面

    post方法对应前端post请求：
        不能通过验证，就返回当前页面
        1、将前端post请求的参数放置在表单中，进行数据合法验证
        2、通过数据合法验证，需要获取相关的数据，获取数据的方式有两种：
            1）获取经过form表单处理的参数：
                register_form.cleaned_data["user"]
                register_form.cleaned_data["pwd"]
                register_form.cleaned_data["code"]
            2）直接获取表单提交的数据
                request.POST.get("user", "")
                request.POST.get("pwd", "")
                request.POST.get("code", "")
        3、最后将获取的数据保存到数据库中，为防止保存到数据库的过程中出现错误，需要使用：
            try:
                ...
            except:
                ...
        4、另外还需要对密码加密，调用make_password()即可
        5、以上四步完成最后渲染前台登录页面
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", context={"form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            try:
                # print(register_form.cleaned_data["pwd"])
                user = User(username=request.POST.get("user", ""),
                            email=request.POST.get("pwd", ""),
                            password=make_password(request.POST.get("pwd", "")))
                user.save()
                return redirect(reverse("user:user_login"))
            except Exception as e:
                print(e)
                return self.get(request)
        else:
            return self.get(request)


class LogoutView(View):
    """
    点击注销或者退出登录或者直接输入注销地址，或删除当前登录用户的所有session值
    """
    def get(self, request):
        # 删除所有的session值
        logout(request)
        return redirect(reverse("user:user_login"))


class ProfileView(View):
    """
    和Flask的基于调度方法的类视图一模一样，
    get方法对应前端get请求：
        获取当前登录用户的信息并渲染到个人中心页面

    post方法对应前端post请求：
        当前页面用户已登录才能post请求，获取前台参数
        1、对前端post请求的参数中的文件信息，需要try: ... except: ...
        2、通过数据合法验证，将获取的参数与数据库数据匹配。django已经提供用户验证，
            从django.contrib.auth中导入authenticate方法
        3、通过用户验证，将user的相关信息保存到session中
        4、以上三步完成最后渲染主页面
    """
    def get(self, request):
        try:
            userinfo = UserInfo.objects.get(user=request.user)
        except:
            userinfo = []
        return render(request, "profile.html", {"userinfo": userinfo})

    def post(self, request):
        if request.user.is_authenticated:
            last_name = request.POST.get("last_name", "")
            gender = request.POST.get("sex", "")
            u = User.objects.get(pk=request.user.id)
            u.last_name = last_name
            u.save()

            try:
                userinfo = UserInfo.objects.get(user=request.user)
                userinfo.gender = gender
                avatar = request.FILES.get("avatar")
                if avatar:
                    userinfo.avatar = avatar
                userinfo.save()
            except:
                avatar = request.FILES.get("avatar", "")
                if avatar:
                    u = UserInfo.objects.create(gender=gender, avatar=avatar, user=request.user)
                else:
                    u = UserInfo.objects.create(gender=gender, avatar="upload/user/2019/avatar.png", user=request.user)
        return self.get(request)
