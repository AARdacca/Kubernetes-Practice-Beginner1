import json

import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from authentication.models import Checkout, User

from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY
from django.http import JsonResponse


def checkout_view(request):
    if request.user.is_authenticated:
        if request.method=="GET":

            return render(request,'checkout.html')
        if request.method=="POST":
            data = request.POST
            cart_data = request.COOKIES.get('cart')
            json_data = json.loads(cart_data)
            print(json_data)
            if json_data:
                pass
            else:
                return redirect('/cart/')
            if data['ques']=="false" :
                messages.error(request,'Please Answer this question correctly.')
                return redirect('/checkout/')
            order = Order.objects.create(date_of_birth = data['dob'],first_name = data['firstName'],last_name = data['lastName'],
                                        country = data['country'],street_address=data['address1'],address_line2=data['address2'],
                                        town = data['city'],postcode = data['postcode'], phone=data['phone'],
                                        email=data['email'])
            

            order.user = request.user
            # Adding Product With Quantity form Cookies.
            for i in json_data:
                try:
                    product = Lottery.objects.get(id = i['id'])
                except:
                    continue
                OrderItem.objects.create(order = order, product=product, quantity = i['quantity'])
            if 'emailUpdates' in data:
                if data['emailUpdates'] == 'on':
                    order.sign_me_up = True

            # Saving The Checkout For Future Use.
            if 'save_checkout' in data:
                if data['save_checkout'] =='on':
                    Checkout.objects.create(user = request.user,date_of_birth = data['dob'],first_name = data['firstName'],last_name = data['lastName'],
                                            country = data['country'],street_address=data['address1'],address_line2=data['address2'],
                                            town = data['city'],postcode = data['postcode'], phone=data['phone'],
                                            email=data['email'])
        return render(request, 'payment.html',context={'order':order})
    else:
        return redirect('/auth/login')




def checkout_with_saved_data(request,pk):
    if request.user.is_authenticated:
        checkout = Checkout.objects.get(id=pk)
        cart_data = request.COOKIES.get('cart')
        json_data = json.loads(cart_data)
        if json_data:
            pass
        else:
            return redirect('/cart/')
        
        order = Order.objects.create(date_of_birth = checkout.date_of_birth,first_name = checkout.first_name,last_name = checkout.last_name,
                                        country = checkout.country,street_address= checkout.street_address,address_line2=checkout.address_line2,
                                        town = checkout.town,postcode = checkout.postcode, phone=checkout.phone,
                                        email=checkout.email)
        order.user = request.user
            
        for i in json_data:
            try:
                product = Lottery.objects.get(id = i['id'])
            except:
                continue
            OrderItem.objects.create(order = order, product=product, quantity = i['quantity'])

        return render(request, 'payment.html',context={'order':order})
    else:
        return redirect('/auth/login')
        
    
def payment_view(request,pk):
    if request.method=='POST':
        try:
            order = Order.objects.get(id=pk)
        except:
            return redirect('/checkout/')
        inline_items = []
        YOUR_DOMAIN = 'http://localhost:8000'
        for i in order.orderitem_set.all():
            print(i.product.price)
            print(i.product.image.url)
            print(f'{YOUR_DOMAIN+str(i.product.image.url)}')
            item ={
             'price_data':{
                    'currency': 'usd',
                    
                    'unit_amount_decimal': (i.product.price *100),
                    'product_data': {
                        'name':i.product.name,
                        'images': [f'{YOUR_DOMAIN+str(i.product.image.url)}']
                    },
                },
                'quantity': i.quantity,
            }
            print(type(item))
            inline_items.append(item)
        print(inline_items)
        
        checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=inline_items,

        mode='payment',
        success_url=YOUR_DOMAIN + f'/checkout/success/{pk}/',
        cancel_url=YOUR_DOMAIN + f'/checkout/cancel/{pk}/',
        )
        return redirect(checkout_session.url, code=303)
    

def success_view(request,pk):
    try:
        order = Order.objects.get(id=pk)
    except:
        return redirect('/')
    order.payment_status = True
    order.save()
    for i in order.orderitem_set.all():
        i.product.total_sold = i.product.total_sold + i.quantity
        i.save()
    return render(request,'success.html', context={'order':order})


def cancel_view(request,pk):
    try:
        order = Order.objects.get(id=pk)
    except:
        return redirect('/')
    order.payment_status = False
    order.save()

    return render(request,'cancel.html', context={'order':order})