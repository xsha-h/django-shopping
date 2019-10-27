from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render


# Create your views here.
from django.views.generic.base import View

from commodity.models import Commodity, CommodityType
from operations.models import Cart


def index(request):
    return render(request, "index.html")


class IndexView(View):
    def get(self, request):
        # 菜单栏
        menus = CommodityType.objects.all()
        # 特别推荐
        introducecommoditys = Commodity.objects.all().order_by("-view_nums")
        # 热门商品
        salenumcommoditys = Commodity.objects.all().order_by("-sale_nums")
        # 新品上架
        newcommoditys = Commodity.objects.all().order_by("-created_time")

        # 男女装服饰
        clothes_type = CommodityType.objects.filter(name="服装")[0]
        clothes = Commodity.objects.filter(Q(one_typename=clothes_type.id) |
                                           Q(two_typename=clothes_type.id) |
                                           Q(three_typename=clothes_type.id))

        # 男女装服饰排行榜
        clothes_rank = clothes.order_by("-created_time")

        # 鞋包服饰
        shoes_type = CommodityType.objects.filter(name="鞋包")[0]
        shoes = Commodity.objects.filter(Q(one_typename=shoes_type.id) |
                                         Q(two_typename=shoes_type.id) |
                                         Q(three_typename=shoes_type.id))

        # 鞋包服饰排行榜
        shoes_rank = shoes.order_by("-created_time")

        # 家具
        furniture_type = CommodityType.objects.filter(name="家具")[0]
        furnitures = Commodity.objects.filter(Q(one_typename=furniture_type.id) |
                                              Q(two_typename=furniture_type.id) |
                                              Q(three_typename=furniture_type.id))

        # 家具排行榜
        furnitures_rank = furnitures.order_by("-created_time")

        # 购物车数量

        # cart_nums = Cart.objects.get(user=request.user).numbers
        res_dict = {
            "menus": menus if len(menus) < 8 else menus[:8],
            "introducecommoditys": introducecommoditys if len(introducecommoditys) < 4 else introducecommoditys[:4],
            "salenumcommoditys": salenumcommoditys if len(salenumcommoditys) < 4 else salenumcommoditys[:4],
            "newcommoditys": newcommoditys if len(newcommoditys) < 4 else newcommoditys[:4],
            "clothes": clothes if len(clothes) < 6 else clothes[:6],
            "shoes": shoes if len(shoes) < 6 else shoes[:6],
            "furnitures": furnitures if len(furnitures) < 6 else furnitures[:6],
            "clothes_rank": clothes_rank if len(clothes_rank) < 3 else clothes_rank[:3],
            "shoes_rank": shoes_rank if len(shoes_rank) < 3 else shoes_rank[:3],
            "furnitures_rank": furnitures_rank if len(furnitures_rank) < 3 else furnitures_rank[:3],
            # "cart_nums": cart_nums,
        }

        return render(request, "index.html", res_dict)


class CommodityDetail(View):
    def get(self, request, id):
        commodity = Commodity.objects.get(id=id)
        commodityfiles = commodity.commoditydisplayfiles_set.all()
        commoditys_sales_rank = Commodity.objects.all().order_by("-sale_nums")
        commoditys_views_rank = Commodity.objects.all().order_by("-view_nums")
        return render(request, "commodity.html", {
            "commodity": commodity,
            "commodityfiles": commodityfiles,
            "commoditys_sales_rank": commoditys_sales_rank if len(commoditys_sales_rank) < 4 else commoditys_sales_rank[:4],
            "commoditys_views_rank": commoditys_views_rank if len(commoditys_views_rank) < 4 else commoditys_views_rank[:4]
        })


class CommodityListView(View):
    def get(self, request, id):
        commodity_lists = Commodity.objects.filter(Q(one_typename_id=id) |
                                                   Q(two_typename_id=id) |
                                                   Q(three_typename_id=id))

        # 分页实现
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(commodity_lists, 4, request=request)

        commodity_lists = p.page(page)
        return render(request, "commodity_lists.html", {
            "commodity_lists": commodity_lists
        })
