from django.shortcuts import render,get_object_or_404
from store.models import Product
from category.models import Category
from accounts.forms import RegistrationForm
from accounts.models import Account
# Create your views here.
def home(request):
    products=Product.objects.all().filter(is_available=True)
    context={'products':products}
    return render(request,'home.html',context)
def cart(request):
    return render(request,'cart.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')







