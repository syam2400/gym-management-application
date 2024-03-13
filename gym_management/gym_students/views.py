from django.shortcuts import get_object_or_404, redirect, render
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


def students_homepage_view(request):
    
    return render(request,"students-index.html")


def students_profile_view(request):
     
    student_user = get_object_or_404(StudentProfile,student =request.user)
    rooms=Room.objects.all()
    return render(request,"student_profile.html",{'student_user':student_user,'rooms': rooms})


def chat_rooms_view(request,slug):
    student_user = get_object_or_404(StudentProfile,student =request.user)
    room_name=Room.objects.get(slug=slug).name
    print(slug,room_name)
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    return render(request,"student_profile.html",{"student_user":student_user,"room_name":room_name, "messages":messages,"slug":slug})




@login_required
def update_user_details(request,pk):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        image = request.FILES.get('image')



        print(username)
        user_obj = get_object_or_404(StudentProfile,pk=pk)
        if image:
            user_obj.student_profile_picture.save(image.name, image)  

        user_obj.student.username=username
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
@login_required
def initiate_payment_view(request):
    total = 1500
   
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
            "name": "gym-app",
            "description": "Payment for Your Product",
            "image": "https://www.onlinelogomaker.com/blog/wp-content/uploads/2017/06/shopping-online.jpg",  # Replace with your logo URL
        }
  
    return render(request,"payment.html",{'data':response_data})



@csrf_exempt 
def payment_success(request):
    
    return render(request, "payment_success.html")

@csrf_exempt
def payment_failed(request):
    return render(request, "payment_failed.html")
