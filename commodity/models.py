from django.db import models


# Create your models here.
# 商品类型类
class CommodityType(models.Model):
    name = models.CharField(verbose_name="分类名称", max_length=20)
    level = models.IntegerField(verbose_name="分类级别")
    uper_type = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta():
        verbose_name = "商品分类信息表"

    def __str__(self):
        return self.name


class Commodity(models.Model):
    name = models.CharField(verbose_name="商品名称", max_length=100)
    original_price = models.FloatField(verbose_name="商品原价")
    actual_price = models.FloatField(verbose_name="商品现价")
    freight = models.FloatField(verbose_name="商品运费")
    image = models.ImageField(verbose_name="商品图片", upload_to="uploads/commodity/%Y/%m/%d")
    detail = models.CharField(verbose_name="商品详情", max_length=300)
    sale_nums = models.IntegerField(verbose_name="商品销量")
    all_nums = models.IntegerField(verbose_name="商品库存")
    comments_nums = models.IntegerField(verbose_name="商品评论量")
    favor_nums = models.IntegerField(verbose_name="商品收藏量")
    view_nums = models.IntegerField(verbose_name="商品浏览量")
    created_time = models.DateTimeField(verbose_name="录入时间")
    one_typename = models.ForeignKey("CommodityType", on_delete=models.CASCADE,
                                     null=True, blank=True, related_name="one")
    two_typename = models.ForeignKey("CommodityType", on_delete=models.CASCADE,
                                     null=True, blank=True, related_name="two")
    three_typename = models.ForeignKey("CommodityType", on_delete=models.CASCADE,
                                       null=True, blank=True, related_name="three")

    class Meta():
        verbose_name = "商品信息表"

    def __str__(self):
        return self.name


class CommodityDisplayFiles(models.Model):
    commodity = models.ForeignKey("Commodity", on_delete=models.CASCADE)
    text = models.CharField(verbose_name="说明", max_length=255)
    commodity_file = models.FileField(verbose_name="展示图", upload_to="uploads/commodity/%Y/%m/%d")

    class Meta():
        verbose_name = "商品文件信息表"

    def __str__(self):
        return self.text
