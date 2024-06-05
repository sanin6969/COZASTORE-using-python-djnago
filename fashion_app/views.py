from django.shortcuts import render
from store.models import Product
from cart.models import CartItem
from .forms import ContactForm
# Create your views here.
def home(request):
    products=Product.objects.all().filter(is_available=True)
    context={'products':products,}
    return render(request,'home.html',context)
def blog(request):
    return render(request,'blogpage/blog.html')
def blogdetails(request,blog_id):
    return render(request,'blogpage/blogdetail.html')

from django.core.mail import send_mail
from django.shortcuts import render, redirect

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)  # Assuming you have a ContactForm class defined

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']  # Assuming 'subject' is a field in ContactForm

            # Craft the email message
            message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{form.cleaned_data['subject']}"  # Assuming 'message' is a field

            try:
                send_mail(
                    message,
                    subject,
                   email,  # Replace with your actual sender email
                    ['muhdsaninev@gmail.com', 'recipient_email2@example.com'],  # Replace with recipient emails (list)
                    fail_silently=False,
                )
                return redirect('success')  # Redirect to a success page (optional)
            except Exception as e:
                print(f"Error sending email: {e}")
                context = {'form': form, 'error_message': 'There was an error sending your message. Please try again later.'}
                return render(request, 'contact.html', context)

        else:
            context = {'form': form}
            return render(request, 'contact.html', context)

    else:
        form = ContactForm()  # Create an empty form for GET requests
        context = {'form': form}
        return render(request, 'contact.html', context)










