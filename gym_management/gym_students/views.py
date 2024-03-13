from django.shortcuts import get_object_or_404, redirect, render
from gym_students.models import *
from django.contrib.auth.decorators import login_required

import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseServerError
import requests



def students_homepage_view(request):
    
    return render(request,"students-index.html")



def students_profile_view(request):
     
    rooms=Room.objects.all()
    student_user = get_object_or_404(StudentProfile,student =request.user)
    return render(request,"student_profile.html",{'student_user':student_user,'rooms':rooms})


def chat_rooms_view(request,slug):
    student_user = get_object_or_404(StudentProfile,student =request.user)
    room_name=get_object_or_404(Room, slug=slug) 
    print(slug,room_name)
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
   
    return render(request,"student_profile.html",{"student_user":student_user,"room_name":room_name, "messages":messages,"slug":slug})

@login_required
def update_user_details(request,pk):
    if request.method == "POST":
        username = request.POST.get('username')
        print(username)
        user_obj = get_object_or_404(StudentProfile,pk=pk)
        user_obj.student.username=username
        user_obj.student.save()
        return redirect('student_profile')

    user = get_object_or_404(StudentProfile,pk=pk)
    return render(request,"edit-user-details.html",{'user': user})



# payment_app/views.py

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


    