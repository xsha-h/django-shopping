from datetime import datetime

from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View
from pure_pagination import Paginator

from commodity.models import Commodity
from operations.models import Cart, Favor, Orders, OrderCommodityShip
from user.models import Address


class FlowListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            # 获取当前用户的商品购物车信息
            carts = Cart.objects.filter(user=request.user)
            all_price = 0
            for cart in carts:
                all_price += cart.numbers*cart.commodity.actual_price
            return render(request, "flow.html", {
                "carts": carts,
                "all_price": all_price,
            })
        else:
            return redirect(reverse("user:user_login"))


class FlowAddView(View):
    def get(self, request, id, nums):
        if request.user.is_authenticated:
            if Cart.objects.filter(commodity=Commodity.objects.get(pk=id)):
                cart = Cart.objects.filter(commodity=Commodity.objects.get(pk=id)).first()
                cart.numbers += nums
                cart.save()
            else:
                cart = Cart()
                cart.numbers = nums
                cart.user = request.user
                cart.created_time = datetime.now()
                commodity = Commodity.objects.get(pk=id)
                cart.commodity = commodity
                cart.save()
            return redirect(reverse("operations:flow"))
        else:
            return redirect(reverse("user:user_login"))


class FlowDeleteView(View):
    def post(self, request):
        id = request.POST.get("cart_id", "")
        cart = Cart.objects.get(pk=int(id))
        cart.delete()
        return redirect(reverse("operations:flow"))


class FavorAddView(View):
    def post(self, request):
        id = request.POST.get("commodity_id", "")
        favor = Favor(user=request.user, commodity=Commodity.objects.get(pk=int(id)), created_time=datetime.now())
        favor.save()
        return redirect(reverse("operations:flow"))


class FavorView(View):
    def get(self, request):
        favors = Favor.objects.all()
        # 分页实现
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(favors, 4, request=request)

        favors = p.page(page)
        return render(request, "favor.html", {"favors": favors})


class AddressView(View):
    def get(self, request, commodity_ids, commodity_nums):
        if request.user.is_authenticated:
            addresss = Address.objects.filter(user=request.user)

            idlist = commodity_ids.split(",")
            numslist = commodity_nums.split(",")

            idlist1 = list(map(int, idlist))
            numslist1 = list(map(int, numslist))
            id_num_dict = dict(zip(idlist1, numslist1))
            print(id_num_dict)
            commoditys = Commodity.objects.filter(pk__in=idlist1)
            all_price = 0
            for commodity in commoditys:
                commodity.nums = id_num_dict[commodity.id]
                all_price += commodity.actual_price*commodity.nums
            return render(request, "address.html", {
                "addresss": addresss,
                "commoditys": commoditys,
                "all_price": all_price
            })


class AddAddressView(View):
    def post(self, request):
        user = request.user
        name = request.POST.get("name", "")
        tel = request.POST.get("tel", "")
        addr = request.POST.get("addr", "")
        postal = request.POST.get("postal", "")
        address = Address(user=user, name=name, tel=tel, addr=addr, postal=postal)
        address.save()
        return HttpResponse(status=200)


class AddOrderView(View):
    def post(self, request):
        if request.user.is_authenticated:
            commodity_ids = request.POST.get("ids")
            commodity_nums = request.POST.get("nums")
            address_id = request.POST.get("address_id")
            all_price = request.POST.get("all_price")

            print(all_price, type(all_price))

            addr = Address.objects.get(pk=int(address_id))
            order = Orders(user=request.user, addr=addr, status=1,
                           order_time=datetime.now(), total_price=float(all_price))
            order.save()

            idlist = commodity_ids.split(",")
            numslist = commodity_nums.split(",")

            idlist1 = list(map(int, idlist))
            numslist1 = list(map(int, numslist))
            id_num_dict = dict(zip(idlist1, numslist1))
            print(id_num_dict)
            commoditys = Commodity.objects.filter(pk__in=idlist1)
            for commodity in commoditys:
                order_detail = OrderCommodityShip(orders=order,
                                                  commodity=commodity,
                                                  numbers=id_num_dict[commodity.id])
                order_detail.save()
            return HttpResponse(status=200)


class OrderView(View):
    def get(self, request):
        orders = Orders.objects.filter(user=request.user).all()

        order_list = []
        # 每条订单记录
        for order in orders:
            # 订单记录的详情
            order_detail = {
                "id": order.id,
                "all_price": order.total_price,
                "state": order.status,
                # 该订单记录下的所有商品
                "commoditys": [],

            }
            order_commoditys = OrderCommodityShip.objects.filter(orders=order).all()
            # 设置商品的数量
            for order_commodity in order_commoditys:
                order_commodity.commodity.nums = order_commodity.numbers
                order_detail["commoditys"].append(order_commodity.commodity)
            order_list.append(order_detail)
        return render(request, "order.html", {
            "order_list": order_list,
        })

