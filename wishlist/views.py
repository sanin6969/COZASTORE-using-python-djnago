from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from store.views import Product
from. models import WishItem,Wishlist
from django.contrib.auth.decorators import login_required

# Create your views here.
def _wish_id(request):
    wish=request.session.session_key
    if not wish:
        wish=request.session.create()
    return wish
def _wish_id(request):
    wish = request.session.session_key
    if not wish:
        wish = request.session.create()
    return wish

def add_wish(request, product_id):
    current_user = request.user
    
    if current_user.is_authenticated and current_user.is_superadmin:
        messages.warning(request, 'admins cannot add items to the Wishlist')
        return redirect('shop')
    
    product = Product.objects.get(id=product_id)
    
    if current_user.is_authenticated:
        try:
            wish = Wishlist.objects.get(wish_id=_wish_id(request))
        except Wishlist.DoesNotExist:
            wish = Wishlist.objects.create(wish_id=_wish_id(request))
            wish.save()
        
        is_wish_item_exists = WishItem.objects.filter(product=product, user=current_user).exists()
        
        if is_wish_item_exists:
            wish_items = WishItem.objects.filter(product=product, user=current_user)
            for item in wish_items:
                item.quantity += 1
                item.save()
        else:
            wish_item = WishItem.objects.create(product=product, quantity=1, wish=wish, user=current_user)
            wish_item.save()
        
        return redirect('wishlist')
# user not guest
    else:
        try:
            wish = Wishlist.objects.get(wish_id=_wish_id(request))
            print('try block')
        except Wishlist.DoesNotExist:
            wish = Wishlist.objects.create(wish_id=_wish_id(request))
            print('else block')
            wish.save()
        
        is_wish_item_exists = WishItem.objects.filter(product=product, wish=wish).exists()
        
        if is_wish_item_exists:
            wish_items = WishItem.objects.filter(product=product, wish=wish)
            for item in wish_items:
                item.quantity += 1
                print(wish_items)
                item.save()
        else:
            wish_item = WishItem.objects.create(product=product, quantity=1, wish=wish)
            print('quntity else')
            wish_item.save()
        
        return redirect('wishlist')


@login_required(login_url='login')          
def wishlist(request,wish_items=None):
    try:
        if request.user.is_authenticated:
            wish_items = WishItem.objects.filter(user=request.user, is_active=True)
        else:
            wish=Wishlist.objects.get(wish_id=_wish_id(request))
            wish_items=WishItem.objects.filter(wish=wish,is_active=True)
    except:
        pass            
    context={
        "wish_items":wish_items,
    }    
    return render(request,'wishlist/wishlist.html',context) 

def delete_wish(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        wish_item=WishItem.objects.get(product=product,user=request.user)
    else:
        wish=Wishlist.objects.get(wish_id=_wish_id(request))
        wish_item=WishItem.objects.get(product=product,wish=wish)
    wish_item.delete()
    return redirect('wishlist')                
                
            