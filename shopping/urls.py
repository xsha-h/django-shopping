"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shopping import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 添加验证码url
    url(r'^captcha/', include("captcha.urls")),

    path('user/', include('user.urls', namespace="user")),    # 用户模块
    path('commodity/', include('commodity.urls', namespace="commodity")),    # 商品模块
    path('operations/', include('operations.urls', namespace="operations")),    # 购物车、收藏夹、订单等模块
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)       # 添加配件文件中配置的上传文件路径
