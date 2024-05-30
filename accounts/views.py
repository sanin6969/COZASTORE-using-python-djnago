from django.shortcuts import render,redirect
from .forms import RegistrationForm,Userform
from .models import Account,UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cart.models import Cart,CartItem
from cart.views import _cart_id
from orders.models import Order
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
            message=render_to_string('verification_email.html',{
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
    return render(request,'register.html',context)


def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user=auth.authenticate(email=email,password=password)
        print(user.id)
        if user.is_superadmin:
            return redirect('adminpage')
        
        
        if user is not None:
            try:
                print('entering try bvlock')
                cart=Cart.objects.get(cart_id=_cart_id(request))
                # is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    
                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                print('entering except')
                pass
            auth.login(request,user)
            messages.success(request,'You are now logged In')
            
            return redirect('home')
        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')     
    
    return render(request,'login.html')


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
            message=render_to_string('reset_password.html',{
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
    return render(request,'forgotpassword.html')



def resetpassword_verify(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return render(request, 'resetpassword.html')
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
        return render(request,'resetpassword.html')
    
    
    
    # DAST BOARD
@login_required(login_url='login')
def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count=orders.count()
    context={
        'orders_count':orders_count
    }
    return render(request,'dashboard.html',context)
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True,).order_by('-created_at')
    context={
        'orders':orders
    }
    return render(request,'myorders.html',context)

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
            
        
    return render(request,'editprofile.html',context)

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
    return render (request,'changepassword.html')