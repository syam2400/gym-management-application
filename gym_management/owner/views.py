from django.shortcuts import get_object_or_404, redirect, render
from users.models import CustomUser



def users_list(request):
    users = CustomUser.objects.all()  
    return render(request,'owner-index.html',{'users': users})

def approve_user(request, user_id):
      
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_approved = True
        user.save()
       
        return redirect('users_list')


def student_details(request):
      student_users =CustomUser.objects.filter(is_student=True)

      return render(request,'student-details.html',{'student_users': student_users})
      
def trainer_details(request):
      trainer_users =CustomUser.objects.filter(is_trainer=True)

      return render(request,'trainer-detail.html',{'trainer_users':  trainer_users})
      

def operations(request):
      return render(request,'operations.html')