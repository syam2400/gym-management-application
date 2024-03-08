from django.shortcuts import render
from gym_students.models import *

def students_homepage_view(request):
    
    return render(request,"students-index.html")

import requests

def students_profile_view(request):
  

    url = "https://exerciseapi3.p.rapidapi.com/exercise/name/push%20up"

    headers = {
        "X-RapidAPI-Key": "cac4259a1emsh8367cb09942567cp1f4ba6jsn9992c6509ff1",
        "X-RapidAPI-Host": "exerciseapi3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data=response.json()

    print(response.json())
    return render(request,"student_profile.html",{"data":  data})

def chat_rooms_view(request):
    rooms=Room.objects.all()
   
    return render(request, "chat-rooms.html",{'rooms':rooms})
  

def room(request,slug):
    room_name=Room.objects.get(slug=slug).name
    print(slug,room_name)
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    
    return render(request,"room.html",{"room_name":room_name, "messages":messages,"slug":slug})