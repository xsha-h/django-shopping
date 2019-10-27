from django.conf.urls import url
from django.urls import path
from . import views

app_name = '[commodity]'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # 无关键字传参
    # url(r"detail/(\d+)", views.CommodityDetail.as_view(), name="commodity_detail"),
    # 关键字传参
    url(r"detail/(?P<id>\d+)", views.CommodityDetail.as_view(), name="commodity_detail"),
    # 上面的url可以改成re_path
    # 另一中传参
    # path("detail/<int: id>/", views.CommodityDetail.as_view(), name="commodity_detail"),

    path("commodity_list/<int:id>/", views.CommodityListView.as_view(), name="commodity_list")
]
