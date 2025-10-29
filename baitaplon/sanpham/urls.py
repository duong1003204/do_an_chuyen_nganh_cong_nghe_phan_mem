
from django.urls import include, path

from nguoidung import views
from .views import chitietsanpham, colors_for_size,image_for_variant, shop, shop_danhmuc

urlpatterns = [
    path('chitietsanpham/<int:id>/', chitietsanpham, name='chitietsanpham'),
    path('ajax/colors/', colors_for_size, name='colors_for_size'),
    path('ajax/image/', image_for_variant, name='image_for_variant'),
    path('shop/', shop, name='shop'),
    path('shop/danhmuc/<int:id>/', shop_danhmuc, name='shop_danhmuc'),
]