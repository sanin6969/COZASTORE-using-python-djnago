from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Account 
from store.models import Category,Product
from django.contrib import messages,auth
from .forms import ProductUpdateForm
from orders.models import Order,OrderProduct
# Create your views here.
def adminpage(request):
    # Initialize variables
    Total_income = 0
    total_products = 0
    out_of_stock = 0
    total_users = 0
    total_orders = 0
    total_cancel = 0
    orders_data = {}

    # Calculate total users
    total_users = Account.objects.count()

    # Calculate out of stock products
    products_available = Product.objects.filter(is_available=True)
    for item in products_available:
        if item.product_stock <= 0:
            out_of_stock += 1

    # Calculate total products in store
    total_products = Product.objects.filter(is_available=True).count()

    # Calculate total orders and cancellations
    orders = Order.objects.all()
    for order in orders:
        Total_income += order.order_total
        Total_income = round(Total_income, 2)
        total_orders += 1

        if order.status == "Cancelled":
            total_cancel += 1

        user_id = order.user.id
        if user_id in orders_data:
            orders_data[user_id]['total_orders'] += 1
            if order.status == "Cancelled":
                orders_data[user_id]['total_cancel'] += 1
        else:
            orders_data[user_id] = {
                'user': order.user,
                'total_orders': 1,
                'product_quantities': {},
                'total_cancel': 1 if order.status == "Cancelled" else 0
            }

        # Calculate product quantities per user
        ordered_products = OrderProduct.objects.filter(order=order)
        for order_product in ordered_products:
            product_name = order_product.product.product_name
            if product_name in orders_data[user_id]['product_quantities']:
                orders_data[user_id]['product_quantities'][product_name] += order_product.quantity
            else:
                orders_data[user_id]['product_quantities'][product_name] = order_product.quantity

    context = {
        "Total_income": Total_income,
        "total_products": total_products,
        "products_available": products_available,
        "out_of_stock": out_of_stock,
        "total_users": total_users,
        "total_orders": total_orders,
        "orders_data": orders_data,
        "total_cancel": total_cancel
    }
    
    return render(request, 'adminpage/admin.html', context)




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
    return render(request,'adminpage/users.html',context)

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
    return render(request,'adminpage/products.html',context)

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

    return render(request,'adminpage/add_product.html',context)

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
    return render(request, "adminpage/add_product.html", context)

def delete_Product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect("products")


# ORDERS
def orders(request):
    
    orders = Order.objects.all().order_by('-created_at')
 
    context = {
        "orders": orders,
    
    }
    return render(request, "adminpage/orders.html", context)

def orderdetails(request,id):
    order = Order.objects.get(id=id)
    details = OrderProduct.objects.filter(order=order)
    print(f"Details: {details}")
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    subtotal = 0
    for i in ordered_products:
        subtotal += i.product_price * i.quantity
    context = {
        "details" : details,
        "order"   : order,
        'ordered_products' : ordered_products,
        'subtotal' : subtotal,
        }
    
    return render(request,'adminpage/orderdetails.html',context)