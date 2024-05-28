from django.shortcuts import render
from store.models import Product
from cart.models import CartItem
# Create your views here.
def home(request):
    products=Product.objects.all().filter(is_available=True)
    context={'products':products,}
    return render(request,'home.html',context)
def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')







