from django.shortcuts import render
from .models import Product,Category
from django.shortcuts import render,get_object_or_404
from cart .models import CartItem
from cart .views import _cart_id
# Create your views here.
def shop(requset,category_slug=None):
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
    return render(requset,'shop.html',context)

def details(request,category_slug,product_slug):
    try:
        category = get_object_or_404(Category, slug=category_slug)
        single_product = get_object_or_404(Product, category=category, product_slug=product_slug)   
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as e:
        raise e
    context={
        'single_product':single_product,
        "in_cart":in_cart
    }
    return render(request,'details.html',context)