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

def cart(request):
    return render(request,'cart.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')

def details(request,category_slug,product_slug):
    try:
        category = get_object_or_404(Category, slug=category_slug)
        single_product = get_object_or_404(Product, category=category, product_slug=product_slug)    
    except Exception as e:
        raise e
    context={
        'single_product':single_product
    }
    return render(request,'details.html',context)

def login(request):
    return render(request,'login.html')




def register(request):
    form=None
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=Account.objects.create_user(username=username,first_name=first_name,last_name=last_name,phone_number=phone_number,email=email,password=password)
            user.phone_number=phone_number
            user.save()
    else:
        form =RegistrationForm()
    context={
        'form':form
    }
    return render(request,'register.html',context)