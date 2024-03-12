from django.shortcuts import get_object_or_404, redirect, render
from gym_students.models import Room,Message

from trainer.models import *

def trainer_homepage(request):
    return render(request,'trainer-index.html')
    
def trainer_profile_view(request):

    trainer_user = get_object_or_404(TrainerProfile,trainer =request.user)
    rooms=Room.objects.all()
    return render(request,"trainer_profile.html",{'trainer_user': trainer_user,"rooms":rooms})



def chat_room(request,slug):
    trainer_user = get_object_or_404(TrainerProfile,trainer =request.user)
    room_name=Room.objects.get(slug=slug).name
    print(slug,room_name)
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    
    return render(request,"trainer_profile.html",{'trainer_user': trainer_user,"room_name":room_name, "messages":messages,"slug":slug})


def update_trainer_details(request,pk):
    
    user = get_object_or_404(TrainerProfile,pk=pk)
    if not request.user.is_authenticated or request.user != user.trainer:
        return redirect('user_login') 
    
    
    return render(request,"edit-trainer-details.html",{'user': user})


