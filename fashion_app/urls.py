from django.urls import path
from . import views
from accounts.views import register,login,userout,activate,dashboard
from store.views import details,shop

urlpatterns = [
    path('',views.home, name='home'),
    
    path('shop',shop, name='shop'),
    
    path('<slug:category_slug>/',shop, name='product_by_category'),
    
    path('<slug:category_slug>/<slug:product_slug>/',details, name='product_detail'),
    
    path('cart',views.cart, name='cart'),
    
    path('blog',views.blog, name='blog'),
    
    path('contact',views.contact, name='contact'),
    
    path('details',details, name='details'),
    
    path('login',login, name='login'),
    
    path('register',register, name='register'),
    
    path('userout',userout, name='userout'),
    
    path('dashboard',dashboard, name='dashboard'),
    
    path('activate/<uidb64>/<token>',activate, name='activate'),
    
    
]
