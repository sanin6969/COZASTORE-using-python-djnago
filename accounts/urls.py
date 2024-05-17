from django.urls import path
from .views import register,login,userout,activate,dashboard,forgotpassword,resetpassword,resetpassword_verify
urlpatterns = [
     path('register',register, name='register'),
     
     path('login',login, name='login'),
     
     path('userout',userout, name='userout'),
     
     path('activate/<uidb64>/<token>',activate, name='activate'),
     
     path('dashboard',dashboard, name='dashboard'),
     
     path('forgotpassword',forgotpassword, name='forgotpassword'),
     
     path('resetpassword',resetpassword, name='resetpassword'),
     
     path('resetpassword_verify/<uidb64>/<token>',resetpassword_verify, name='resetpassword_verify'),
]
