from django.shortcuts import get_object_or_404, redirect, render
from users.custom_decorator import resist_pages
from gym_students.models import *
from django.contrib.auth.decorators import login_required
from gym_students.models import Room,Message
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseServerError
import requests
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.cache import never_cache
from django.db import IntegrityError


@never_cache
@resist_pages
@login_required
def students_homepage_view(request):
    return render(request,"students-index.html")

@never_cache
@resist_pages
@login_required
def students_profile_view(request):
    student_user = get_object_or_404(StudentProfile,student =request.user)
    rooms=Room.objects.all()
    return render(request,"student_profile.html",{'student_user':student_user,'rooms': rooms})


@never_cache
@resist_pages
@login_required
def chat_rooms_view(request,slug):
    student_user = get_object_or_404(StudentProfile,student =request.user)
    room_name=Room.objects.get(slug=slug).name
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    return render(request,"student_profile.html",{"student_user":student_user,"room_name":room_name, "messages":messages,"slug":slug})





@never_cache
@resist_pages
@login_required
def update_user_details(request,pk):
    if request.method == "POST":
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        image = request.FILES.get('image')



        user_obj = get_object_or_404(StudentProfile,pk=pk)
        if image:
            user_obj.student_profile_picture.save(image.name, image)  

      
        user_obj.student.first_name=first_name
        user_obj.student.last_name=last_name
        user_obj.student.email=email
        user_obj.student.address=address
        user_obj.student_bio = bio
        print(user_obj.student_bio)
        user_obj.student.phone=phone
        user_obj.save()
        user_obj.student.save()
        return redirect('student_profile')

    user = get_object_or_404(StudentProfile,pk=pk)
    return render(request,"edit-user-details.html",{'user': user})




# payment_app/views.py


@never_cache
@resist_pages
@login_required
def initiate_payment_view(request):
    total = 1500
   
    amount = float(total) * 100  # Amount in paise
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

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
            "key": settings.RAZORPAY_KEY_ID,
            "name": "gym-app",
            "description": "Payment for Your Product",
            "image": "https://www.onlinelogomaker.com/blog/wp-content/uploads/2017/06/shopping-online.jpg",  # Replace with your logo URL
        }
    callback = 'http://' + str(get_current_site(request)) + '/gym-students/payment-success/'
    current_user = get_object_or_404(CustomUser,username=request.user)
    user = get_object_or_404(StudentProfile,student=current_user)

    order_obj = Order.objects.create(Student_user=user, total_amount=response_data['amount'], order_id=response_data['id'])


    return render(request,"payment.html",{'data':response_data,"callback":callback,'user': user})




@never_cache
@csrf_exempt
@resist_pages
@login_required
def payment_success(request):
     if request.method == "POST":
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            order_details = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
          
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            try:
                client.utility.verify_payment_signature(order_details)

                current_user = get_object_or_404(CustomUser,username=request.user)
                user = get_object_or_404(StudentProfile,student=current_user)
                order_obj = get_object_or_404(Order, Student_user=user)
                
                order_obj.is_payemnt_success = True
                order_obj.total_amount =  1500
                order_obj.razorpay_order_id = order_details['razorpay_order_id']
                order_obj.razorpay_payment_id = order_details['razorpay_payment_id']
                order_obj.razorpay_signature = order_details['razorpay_signature']
                order_obj.save()

                return render(request, "payment_success.html")
            except:
               return render(request, "payment_failed.html")


@never_cache
@csrf_exempt
@resist_pages
@login_required
def payment_details_view(request,pk):
    user_obj = get_object_or_404(StudentProfile,pk=pk)
    user_order_details = Order.objects.filter(Student_user=user_obj)

    return render(request, "payment_details.html",{'user_order_details':user_order_details})