from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="收货人姓名", max_length=100)
    tel = models.CharField(verbose_name="联系方式", max_length=20)
    addr = models.CharField(verbose_name="详细地址", max_length=255)
    postal = models.IntegerField(verbose_name="邮政编码")
    is_default = models.BooleanField(verbose_name="默认地址", default=False)

    class Meta():
        verbose_name = "收获地址"

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """
    与内置的用户表建立一对一的关系
    """
    GENDER_CHOICE = (
        (1, "女"),
        (2, "男"),
        (3, "保密"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.IntegerField(choices=GENDER_CHOICE, verbose_name="性别")
    avatar = models.ImageField(upload_to="upload/user/%Y", verbose_name="头像")
