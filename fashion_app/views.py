from django.shortcuts import render
from store.models import Product
from cart.models import CartItem
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
# Create your views here.
def home(request):
    products=Product.objects.all().filter(is_available=True)
    context={'products':products,}
    return render(request,'home.html',context)
def blog(request):
    return render(request,'blogpage/blog.html')
def blogdetails(request,blog_id):
    return render(request,'blogpage/blogdetail.html')



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            
            # Send email
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=subject,
                from_email=email, 
                recipient_list=['muhdsaninev@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')
        else:
            messages.error(request, "There was an error in your form. Please try again.")
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact.html', context)









