from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Account 
from store.models import Category,Product
from django.contrib import messages,auth
from .forms import ProductUpdateForm
# Create your views here.
def adminpage(request):
    
    return render(request,'admin.html')


# USERS 
def blockuser(request,id):
    block_user=Account.objects.get(id=id)
    if block_user.is_superadmin:
        messages.error(request,'Cannot block superadmin')
    else:
        if block_user.is_blocked:
            block_user.is_blocked = False
            messages.success(request,f"{block_user.username} has been unblocked")
            block_user.save()
        else:
            block_user.is_blocked=True
            messages.success(request,f"{block_user.username}has been blocked")
            block_user.save()
    return redirect('users')
def users(request):
    users=Account.objects.all()
    context = {
            'users': users,
        }
    return render(request,'users.html',context)

def logoutadmin(request):
    auth.logout(request)
    messages.success(request,'You are successfully logged out')
    return redirect('home')



# PRODUCTS
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

def add_product(request):
    if request.method== "POST":
        form=ProductUpdateForm(request.POST,request.FILES)
        print(form.data) 
        if form.is_valid():
            form.save()
            messages.success(request,'Product is added')
            return redirect('products')
    else:
        form = ProductUpdateForm()
    context={
        'form':form
    }

    return render(request,'add_product.html',context)

def edit_product(request,id):
    product=Product.objects.get(id=id)
    
    if request.method == "POST":
        print(request.POST)
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product edited successfully.')
            return redirect("products")
    else:
        form = ProductUpdateForm(instance=product)

    context = {
        "form": form, 
    }
    return render(request, "add_product.html", context)

def delete_Product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect("products")