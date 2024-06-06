from django.urls import path
from .views import adminpage,users,products,logoutadmin,blockuser,add_product,edit_product,delete_Product,orders,orderdetails,category,add_category,edit_category,delete_category
urlpatterns = [
     path('adminpage',adminpage, name='adminpage'),
     path('users',users, name='users'),
     
     path("category/", category, name="category"),
     path("add_category/",add_category, name="add_category"),
     path("<str:slug>/edit_category/", edit_category, name="edit_category"),
     path("<str:slug>/delete_category/", delete_category, name="delete_category"),
     
     path('logoutadmin',logoutadmin, name='logoutadmin'),
     path("<int:id>/blockuser/", blockuser, name="blockuser"),
     path("orders", orders, name="orders"),
     
     path('products',products, name='products'),
     path("add_product/", add_product, name="add_product"),
     path("<int:id>/edit_product/", edit_product, name="edit_product"),
     path("<int:id>/delete_Product/", delete_Product, name="delete_Product"),
     path('<int:id>/orderdetails/',orderdetails,name='orderdetails'),
]