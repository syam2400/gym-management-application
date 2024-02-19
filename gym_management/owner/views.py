from django.shortcuts import get_object_or_404, redirect, render
from users.models import CustomUser



def users_list(request):
    users = CustomUser.objects.all()  
    return render(request,'owner-index.html',{'users': users})

def approve_user(request, user_id):
    # if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_approved = True
        user.save()
        return redirect('users_list')