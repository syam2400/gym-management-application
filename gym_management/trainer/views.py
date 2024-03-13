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
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        image = request.FILES.get('image')

    
        user_obj = get_object_or_404(TrainerProfile,pk=pk)
        if image:
            user_obj.trainer_profile_picture.save(image.name, image) 
        user_obj.trainer.username=username
        user_obj.trainer.first_name=first_name
        user_obj.trainer.last_name=last_name
        user_obj.trainer.email=email
        user_obj.trainer.address=address
        user_obj.trainer_bio = bio
       
        user_obj.trainer.phone=phone
        user_obj.save()
        user_obj.trainer.save()
        return redirect('trainer_profile')
    
    
    return render(request,"edit-trainer-details.html",{'user': user})


