from django.shortcuts import render,redirect
from .forms import RegistrationForm,Userform
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cart.models import Cart,CartItem
from cart.views import _cart_id
from orders.models import Order,OrderProduct
from django.shortcuts import get_object_or_404
# verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone_number = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()
            
            # USER ACTIVATION
            current_site=get_current_site(request)
            print(f'current_site: {current_site}')
            mail_subject='Please activate your account'
            message=render_to_string('Accounts/verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
             
            messages.success(request,'Thank you for registering with us, click on the verification email we have sent')
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request,'Accounts/register.html',context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            if user.is_superadmin:
                return redirect('adminpage')
            elif user.is_blocked:
                messages.error(request,'You were Blocked by Admin')
                
            else:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_items = CartItem.objects.filter(cart=cart)
                        
                        for item in cart_items:
                            item.user = user
                            item.save()
                except Cart.DoesNotExist:

                    pass
                
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    
    return render(request, 'Accounts/login.html')


@login_required(login_url='login')
def userout(request):
    auth.logout(request)
    messages.success(request,'You are successfully logged out')
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congragulation Your account is activated')
        return redirect('login')
    else:
        messages.error(request,'invalid activation link')
        return redirect('register')
    
    




def forgotpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            
            # reset password 
            current_site=get_current_site(request)
            mail_subject='Please reset your pasword'
            message=render_to_string('Accounts/reset_password.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            messages.success(request,'Email for reset password has send to '+email)
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotpassword')
    return render(request,'Accounts/forgotpassword.html')



def resetpassword_verify(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return render(request, 'Accounts/resetpassword.html')
    else:
        messages.error(request, 'This link is expired')
        return redirect('forgotpassword')
            
            
def resetpassword(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['repeat_password']
        
        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password changed,please login')
            return redirect('login')
        else:
            messages.error(request,'Password does not match')
            return redirect('resetpassword')
    else:
        return render(request,'Accounts/resetpassword.html')
    
    
    
    # DAST BOARD
@login_required(login_url='login')
def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count=orders.count()
    context={
        'orders_count':orders_count
    }
    return render(request,'dashboard/dashboard.html',context)


@login_required(login_url='login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True,).order_by('-created_at')
    context={
        'orders':orders
    }
    return render(request,'dashboard/myorders.html',context)


def myorderdetails(request,order_id):
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    context={
        'order_detail':order_detail,
        'order':order
    }
    return render(request,'dashboard/myorderdetails.html',context)

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()

        order_products = OrderProduct.objects.filter(order=order)
        
        for item in order_products:
            # product quantity refunded
            product = item.product
            product.product_stock += item.quantity
            product.save()
            print('product updated')
   
            # income refunded
            Order_total=order.order_total
            
            print('Before',Order_total)
            
            tax=item.order.tax
            
            print('tax',tax)
            
            print('amount of product',(item.product_price*item.quantity))
            
            Order_total-=((item.product_price*item.quantity))
            
            print( 'before tax',Order_total)
            
            
            print('BEFORE SAVE ',Order_total)
            
            order.order_total = Order_total
            
            order.save()
            
            print('after',order.order_total)
            
        Order_total-=tax
            
        print('BEFORE  TAX SAVE ',Order_total)
            
        order.order_total = round(Order_total)
        print('AFTER TAX SAVE ',Order_total)
            
        order.save()
            
        print('AFTER  TAX SAVE ',Order_total)
            
            
        messages.info(request,'order has been cancelled')
    return redirect('myorders')
    
@login_required(login_url='login')
def edit_profile(request):
    # userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method=="POST":
        user_form = Userform(request.POST,instance=request.user)
        # profile_form = Userprofileform(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,'your profile has been updated')
            return redirect('editprofile')
    else:
        user_form=Userform(instance=request.user)
        
    context={
        'user_form':user_form,
        
    }
            
        
    return render(request,'dashboard/editprofile.html',context)

@login_required(login_url='login')
def change_password(request):
    if request.method=="POST":
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        
        user=Account.objects.get(username__exact=request.user.username)
        if new_password== confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Your password has been updated')
                return redirect('changepassword')
            else :
                messages.error(request,'invalid current password')
                return redirect('changepassword')
        else:
            messages.error(request,'Password does not match')
            return redirect('changepassword')
    return render (request,'dashboard/changepassword.html')