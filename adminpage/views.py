from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Account 
from store.models import Category,Product
from django.contrib import messages,auth
# Create your views here.
def adminpage(request):
    
    return render(request,'admin.html')
def users(request):
    users=Account.objects.all()
    context = {
        'users': users,
    }
    return render(request,'users.html',context)


def products(request,category_slug=None):
    categories=None
    products=None
    
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        product_count=products.count()
    else:
        products=Product.objects.all().filter(is_available=True)
        product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
        }
    return render(request,'products.html',context)
def logoutadmin(request):
    auth.logout(request)
    messages.success(request,'You are successfully logged out')
    return redirect('home')