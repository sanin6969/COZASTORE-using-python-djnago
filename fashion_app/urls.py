from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    
    path('blog',views.blog, name='blog'),
    
    path('blogdetails/<int:blog_id>',views.blogdetails, name='blogdetails'),
    
    path('contact',views.contact, name='contact'),
]
