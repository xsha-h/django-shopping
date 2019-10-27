from django.conf.urls import url
from django.urls import path
from . import views

app_name = '[operations]'
urlpatterns = [
    path("flow/", views.FlowListView.as_view(), name="flow"),
    path("add_flow/<int:id>/<int:nums>", views.FlowAddView.as_view(), name="add_flow"),   # 添加购物车
    path("delete_flow", views.FlowDeleteView.as_view(), name="delete_flow"),     # 删除购物车
    path("add_favor", views.FavorAddView.as_view(), name="add_favor"),    # 添加收藏
    path("favor", views.FavorView.as_view(), name="favor"),     # 显示收藏夹
    path("address/<str:commodity_ids>/<str:commodity_nums>", views.AddressView.as_view(), name="address"),  # 跳转到订单的地址界面（并没有真正的存储订单）
    path("add_addr/", views.AddAddressView.as_view(), name="add_addr"),    # 添加地址
    path("add_order/", views.AddOrderView.as_view(), name="add_order"),    # 添加订单
    path("order/", views.OrderView.as_view(), name="order"),     # 订单页面
]
