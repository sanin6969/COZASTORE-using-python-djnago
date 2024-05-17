from django.urls import path
from .views import cart,add_cart

urlpatterns = [
    path('cart',cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
]