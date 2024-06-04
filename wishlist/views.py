from django.shortcuts import render,redirect
from django.contrib import messages
from store.views import Product
from. models import WishItem,Wishlist
# Create your views here.
def _wish_id(request):
    wish=request.session.session_key
    if not wish:
        wish=request.session.create()
    return wish
def add_wish(request,product_id):
    current_user=request.user
    if current_user.is_authenticated and current_user.is_superadmin:
        messages.warning(request,'admins cannot add items to the Wishlist')
        return redirect('shop')
    product=Product.objects.get(id=product_id)
    
    if current_user.is_authenticated:
        try:
            wish=Wishlist.objects.get(wish_id=_wish_id(request))
        except wish.DoesNotexist:
            wish=Wishlist.objects.create(wish_id=_wish_id(request))
            wish.save()
            is_wish_item_exists=WishItem.objects.filter(product=product,user=current_user).exists()
            
            if is_wish_item_exists:
                wish_items=WishItem.objects.filter(product=product,user=current_user)
                for item in wish_items:
                    item.quantity+=1
                    item.save()
                else:
                    wish_item = WishItem.objects.create(product = product,quantity = 1,wish = wish,)
                    wish_item.save()
        return redirect('wishlist')
           
# user not authenticated
    else:
        try:
            wish=Wishlist.objects.get(wish_id=_wish_id(request))
        except wish.DoesNotexist:
            wish = Wishlist.objects.create(wish_id = _wish_id(request))
            wish.save()
            
            is_wish_item_exists=WishItem.objects.filter(product=product,wish=wish).exists()
        if is_wish_item_exists:
            wish_items = WishItem.objects.filter(product = product,wish=wish)
            for item in wish_items:
                item.quantity+=1
                item.save()
        else:
            wish_item=WishItem.objects.create(product=product,quantity=1,wish=wish,)
            wish_item.save()
            return redirect('wishlist')            
            
            
                    
                
                
            