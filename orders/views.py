from django.shortcuts import render,redirect
from cart.models import CartItem
from .models import Order,Payment,OrderProduct
from .forms import OrderForm
import datetime
import json
from django.contrib import messages
# Create your views here.

def place_order(request,total=0,quantity=0):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('shop')

    grand_total=0
    tax=0
    for cart_item in cart_items:
        total+=(cart_item.product.product_price*cart_item.quantity)
        quantity+=cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax

    if request.method =='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user               = current_user
            data.first_name         = form.cleaned_data['first_name']
            data.last_name          = form.cleaned_data['last_name']
            data.phone              = form.cleaned_data['phone']
            data.email              = form.cleaned_data['email']
            data.address_line_1     = form.cleaned_data['address_line_1']
            data.address_line_2     = form.cleaned_data['address_line_2']
            data.country            = form.cleaned_data['country']
            data.state              = form.cleaned_data['state']
            data.city               = form.cleaned_data['city']
            data.pincode            = form.cleaned_data['pincode']
            data.order_note         = form.cleaned_data['order_note']
            data.order_total        = grand_total
            data.tax                = tax
            data.ip                 = request.META.get('REMOTE_ADDR')
            data.save()
            
            # order mumber
            year = int(datetime.date.today().strftime('%Y'))
            date = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            d = datetime.date(year,month,date)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'tax':tax,
                'grand_total':grand_total,
                'total':total
            }
            return render(request,'payments.html',context)
    else:
        return redirect('checkout')  
     
def payments(request):
    body=json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    print(order)
    
    # store transaction details
    payment =Payment(
        user= request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    
    # move the cart items to order product table
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product_id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.product_price
        orderproduct.ordered=True
        orderproduct.save()
        
    # reduce the quanntity of the sold product
    
    # clear the cart
    
    # send email to the the customer
    
    # send order number and paymet details back to sendData method
    
    return render(request,'payments.html')