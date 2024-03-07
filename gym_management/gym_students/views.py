from django.shortcuts import render
from gym_students.models import *

def students_homepage(request):
    rooms=Room.objects.all()
    return render(request, "students-index.html",{"rooms":rooms})



def room(request,slug):
    room_name=Room.objects.get(slug=slug).name
    print(slug,room_name)
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    
    return render(request, "room.html",{"room_name":room_name,"slug":slug,'messages':messages})