from django.urls import path
from .views import register,login,userout,activate,dashboard,forgotpassword,resetpassword,resetpassword_verify,my_orders,edit_profile,change_password,myorderdetails,cancel_order
urlpatterns = [
     path('register',register, name='register'),
     
     path('login',login, name='login'),
     
     path('userout',userout, name='userout'),
     
     path('activate/<uidb64>/<token>',activate, name='activate'),
     
     path('dashboard',dashboard, name='dashboard'),
     
     path('forgotpassword',forgotpassword, name='forgotpassword'),
     
     path('resetpassword',resetpassword, name='resetpassword'),
     
     path('myorders',my_orders, name='myorders'),
     
     path('myorderdetails/<int:order_id>/',myorderdetails, name='myorderdetails'),
     
     path('cancel_order/<int:order_id>/',cancel_order, name='cancel_order'),
     
     path('editprofile',edit_profile, name='editprofile'),
     
     path('changepassword',change_password, name='changepassword'),
     
     path('resetpassword_verify/<uidb64>/<token>',resetpassword_verify, name='resetpassword_verify'),
]
