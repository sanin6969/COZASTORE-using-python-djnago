from django.urls import path
from .views import add_wish,wishlist,delete_wish

urlpatterns = [
        path('add_wish/<int:product_id>/', add_wish, name='add_wish'),
        path('wishlist', wishlist, name='wishlist'),
        path('delete_wish/<int:product_id>/', delete_wish, name='delete_wish'),
]