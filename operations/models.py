from django.contrib.auth.models import User
from django.db import models

from commodity.models import Commodity
from user.models import Address


# Create your models here.
class Orders(models.Model):
    ORDER_STATUS = (
        (1, "未付款"),
        (2, "待发货"),
        (3, "运输中"),
        (4, "已签收")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addr = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name="订单状态", choices=ORDER_STATUS)
    order_time = models.DateTimeField(verbose_name="下单时间")
    total_price = models.FloatField(verbose_name="订单总价")

    class Meta():
        verbose_name = "订单表"

    def __str__(self):
        return self.status


class OrderCommodityShip(models.Model):
    orders = models.ForeignKey("Orders", on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    numbers = models.IntegerField(verbose_name="总数")

    class Meta():
        verbose_name = "订单详情表"

    def __str__(self):
        return self.numbers


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    numbers = models.IntegerField(verbose_name="购物车添加数")
    created_time = models.DateTimeField(verbose_name="添加时间")

    class Meta():
        verbose_name = "购物车信息表"

    def __str__(self):
        return str(self.numbers)


class Favor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    created_time = models.DateTimeField(verbose_name="添加时间")

    class Meta():
        verbose_name = "收藏夹信息表"

    def __str__(self):
        return self.created_time


class Comments(models.Model):
    STAR = (
        (1, "一星级"),
        (2, "二星级"),
        (3, "三星级"),
        (4, "四星级"),
        (5, "五星级")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    orders = models.ForeignKey('Orders', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name='评论')
    star = models.IntegerField(choices=STAR, verbose_name='星级')
    created_time = models.DateTimeField("添加时间")

    class Meta():
        verbose_name = '评论'

    def __str__(self):
        return self.text
