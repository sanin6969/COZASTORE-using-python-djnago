from django.urls import path
from .views import adminpage,users,products,logoutadmin,blockuser,add_product,edit_product,delete_Product
urlpatterns = [
     path('adminpage',adminpage, name='adminpage'),
     path('users',users, name='users'),
     path('products',products, name='products'),
     path('logoutadmin',logoutadmin, name='logoutadmin'),
     path("<int:id>/blockuser/", blockuser, name="blockuser"),
     path("add_product/", add_product, name="add_product"),
     path("<int:id>/edit_product/", edit_product, name="edit_product"),
     path("<int:id>/delete_Product/", delete_Product, name="delete_Product"),
]