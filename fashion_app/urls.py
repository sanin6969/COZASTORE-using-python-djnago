from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    
    path('shop',views.shop, name='shop'),
    
    path('<slug:category_slug>/',views.shop, name='product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.details, name='product_detail'),
    
    path('cart',views.cart, name='cart'),
    
    path('blog',views.blog, name='blog'),
    
    path('contact',views.contact, name='contact'),
    
    path('details',views.details, name='details'),
    
    path('login',views.login, name='login'),
    
]
