from django.contrib import admin


# Register your models here.
from commodity.models import Commodity, CommodityType, CommodityDisplayFiles

admin.site.register(Commodity)
admin.site.register(CommodityType)
admin.site.register(CommodityDisplayFiles)
