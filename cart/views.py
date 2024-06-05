from django.shortcuts import render,redirect,get_object_or_404
from store.views import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, product_id):
    # if request.method=='POST':
    #     color=request.POST['color']
    #     size=request.POST['size']
    #     print(color,size)
        
    current_user=request.user
    if current_user.is_authenticated and current_user.is_superadmin:
        messages.warning(request,"admins cannot add items to the cart.")
        return redirect("shop")
    product = Product.objects.get(id=product_id)
    

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
        is_cart_item_exists = CartItem.objects.filter(product = product,user=current_user).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product,user=current_user)
            for item in cart_items:
                item.quantity += 1
                if item.product.product_stock<item.quantity:
                    messages.error(request,'Product is not available for this quantity')
                else:
                    item.save()
        else:
            cart_item = CartItem.objects.create(product = product,quantity = 1,user = current_user,cart = cart,)
            cart_item.save()
        return redirect('cart')

    # if the user is not authenticated
    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product = product,cart = cart).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product = product,cart=cart)
            for item in cart_items:
                item.quantity += 1
                if item.product.product_stock<item.quantity:
                    messages.error(request,'Product is not available for this quantity')
                else:
                    item.save()

        else:
            cart_item = CartItem.objects.create(product = product,quantity = 1,cart = cart,)
            cart_item.save()
        return redirect("cart")
    # try:
    #       cart_item = CartItem.objects.get(product=product,user=request.user)
    #     else: 
    #         cart_item = CartItem.objects.get(product=product, cart=cart)
    #     cart_item.quantity += 1
    #     cart_item.save()
    # except CartItem.DoesNotExist:  
    #     cart_item = CartItem.objects.create(
    #         product=product,
    #         quantity=1,
    #         cart=cart
    #     )
    #     cart_item.save()
    
    # return redirect('cart')

def sub_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, product=product, user=request.user)
    else:
        cart = get_object_or_404(Cart, cart_id=_cart_id(request))
        cart_item = get_object_or_404(CartItem, product=product, cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        messages.success(request, 'Product removed from the cart.')
    
    return redirect('cart')

def delete_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


from django.core.exceptions import ObjectDoesNotExist

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        product_stock_issues = []
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            print('authenticated')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            print('guest')
        
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity) 
            quantity += cart_item.quantity
            
            # Check product stock
            if cart_item.quantity > cart_item.product.product_stock:
                product_stock_issues.append(cart_item.product)

        tax = (2.5 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'product_stock_issues': product_stock_issues  
    }
    return render(request, 'cart/showcart.html', context)



@login_required(login_url='login')
def checkout(request,total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            print('authencated')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity) 
            quantity += cart_item.quantity
            
        tax=(2.5*total)/100
        grand_total=total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'cart/checkout.html',context)