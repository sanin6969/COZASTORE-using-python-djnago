from django.urls import path
from .views import cart,add_cart,sub_cart,delete_cart

urlpatterns = [
    path('cart',cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('sub_cart/<int:product_id>/', sub_cart, name='sub_cart'),
    path('sub_cart/<int:product_id>/', sub_cart, name='sub_cart'),
    path('delete_cart/<int:product_id>/', delete_cart, name='del_cart'),
]