
from django.shortcuts import render, redirect
from shop.models import Products, Product_features
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.models import Cart, Order , OrderItem

import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseServerError
import requests


@login_required
def cartview(request):
    total = 0
    user = request.user
    try:
        cart = Cart.objects.filter(user=user)
        for i in cart:
            total += i.quantity * i.cart_products.price

    except Cart.DoesNotExist:
        pass
    cart = Cart.objects.filter(user=user)
    return render(request, 'cartview.html', {'cart': cart, 'total': total})


@login_required
def add_to_cart(request, pk):
    p =  Product_features.objects.filter(item=pk).first()
    user = request.user
    try:
        cart = Cart.objects.get(user=user, cart_products=p)
        if (cart.quantity < cart.cart_products.stock):
            cart.quantity += 1
        cart.save()
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user, cart_products=p, quantity=1)
        cart.save()

    return redirect('cart:cartview')


# def add_to_cart(request, p):
#     k = Cart.objects.get(id=p)
#     k.quantity += 1
#     k.save()
#     return redirect('cart:cartview')

# def cart_remove(request, p):
#     k = Cart.objects.get(id=p)
#     k.quantity -= 1
#     k.save()
#     return redirect('cart:cartview')


@login_required
def cart_remove(request, p):
    p = Product_features.objects.get(id=p)
    user = request.user
    try:
        cart = Cart.objects.get(user=user, cart_products=p)
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart:cartview')


@login_required
def full_remove(request, k):
    p = Product_features.objects.get(id=k)
    user = request.user
    try:
        cart = Cart.objects.get(user=user, cart_products=p)
        cart.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cartview')



def cart_checkout(request):
     try:
        previous_order = Order.objects.filter(user=request.user).first()
        if previous_order:
                # Fetch previously entered order details
            address = previous_order.address
            phone = previous_order.phone

        if request.method == 'POST':
            address = request.POST['address']
            phone = request.POST['phone']
            if not address or not phone:
                error_message = "Please provide both address and phone number."
                return render(request, 'checkout.html', {'error_message': error_message})
            
            if previous_order:
                # Update existing order details
                previous_order.address = address
                previous_order.phone = phone
                previous_order.save()
            else:
                user_order = Order.objects.create(user=request.user, address=address, phone=phone)
                user_ordered_products = Cart.objects.filter(user=request.user)
                total_items = 0
                
                for cart_item in user_ordered_products:
                    order_item = OrderItem.objects.create(order=user_order,ordered_products=cart_item.cart_products,quantity=cart_item.quantity)
                    total_items += cart_item.quantity
                
                # Update the order with the total number of items
                user_order.no_of_items = total_items
                user_order.save()
            return initiate_payment(request)
        else:          
            if not previous_order:
                address = ''
                phone = ''        
            total = 0
            cart_items = Cart.objects.filter(user=request.user)
            for items in cart_items:
              total += items.subtotal()
       
            return render(request, 'checkout.html', {'cart':  cart_items, 'total': total,'address': address, 'phone': phone})
     except requests.exceptions.RequestException as e:
         error_message = "Internet connection error occurred. Please check your internet connection and try again."
         return render(request, 'error.html', {'error_message': error_message})

 



# payment_app/views.py
@login_required
def initiate_payment(request):
    total = 0
    user_cart = Cart.objects.filter(user=request.user)
    for i in user_cart:
        total += i.quantity * i. cart_products.price

    amount = float(total) * 100  # Amount in paise
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))

    payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt01",
          }

    order = client.order.create(data=payment_data)
    
        # Include key, name, description, and image in the JSON response
    response_data = {
            "id": order["id"],
            "amount": int(order["amount"])/100,
            "currency": order["currency"],
            "key": settings.KEY,
            "name": "ASHION",
            "description": "Payment for Your Product",
            "image": "https://www.onlinelogomaker.com/blog/wp-content/uploads/2017/06/shopping-online.jpg",  # Replace with your logo URL
        }
  
    user_order_details = Order.objects.get(user=request.user)
    return render(request, "payment.html",{'data':response_data,'user_order_details':user_order_details})


@csrf_exempt
def payment_success(request):
    user_current_cart_items = Cart.objects.filter(user=request.user) 
    user_current_cart_items.delete()
    return render(request, "payment_success.html")
@csrf_exempt
def payment_failed(request):
    return render(request, "payment_failed.html")



















# @login_required
# def checkout(request):
#     # total = 0
#     # if (request.method == 'POST'):
#     #     a = request.POST['a']
#     #     p = request.POST['p']
#     #     n = request.POST['n']
#     #     user = request.user
#     #     cart = Cart.objects.filter(user=user)
#     #     for i in cart:
#     #         total += i.quantity * i.product.price
#     #         ac = Account.objects.get(acc_number=n)
#     #         if (ac.amount >= total):
#     #             ac.amount = ac.amount - total
#     #             ac.save()
#     #             for i in cart:
#     #                 o = Order.objects.create(user=user, products=i.product, address=a, phone=p, order_status='paid',
#     #                                          no_of_items=i.quantity)
#     #                 o.save()
#     #                 i.product.stock = i.product.stock - i.quantity
#     #                 i.product.save()
#     #             cart.delete()
#     #             msg = 'Order Placed Successfully'
#     #             return render(request, 'callback.html', {'msg': msg})
#     #         else:
#     #             msg = 'Insufficient amount,You cannot place order'
#     #             return render(request, 'callback.html', {'msg': msg})
#     cart = Cart.objects.all()
#     return render(request, 'checkout.html', {'cart': cart})
