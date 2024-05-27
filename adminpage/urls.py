from django.urls import path
from .views import adminpage,users,products,logoutadmin
urlpatterns = [
     path('adminpage',adminpage, name='adminpage'),
     path('users',users, name='users'),
     path('products',products, name='products'),
     path('logoutadmin',logoutadmin, name='logoutadmin'),
]