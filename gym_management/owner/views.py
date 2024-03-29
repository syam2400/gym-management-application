from django.shortcuts import get_object_or_404, redirect, render
from users.custom_decorator import resist_pages
from users.models import *
from trainer.models import *
from gym_students.models import *
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from owner.models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from users.custom_decorator import resist_pages



@never_cache
@resist_pages
@login_required
def users_list(request):
    trainer_users = CustomUser.objects.filter(is_trainer=True)
    student_user = CustomUser.objects.filter(is_student=True)
    context = {
         'trainer_users': trainer_users,
         'student_users':student_user
    }
    return render(request,'owner-index.html',context)

# for approving registered user to login,without approval user cant login


def approve_user(request, user_id,):  
        if request.method == 'POST':
            status = request.POST.get('status')
            if status == 'approve':

                  user = get_object_or_404(CustomUser, id=user_id)
                  
                  user.is_approved = True
                  user.save()
                  if user.is_trainer:
                    TrainerProfile.objects.get_or_create(trainer=user)
                  elif user.is_student:
                    StudentProfile.objects.get_or_create(student=user)
                  else:
                    return render(request,'owner-index.html',{'message':'invalid user entry'})         
                  return redirect('users_list')
            elif status == 'rejected':
                  user = get_object_or_404(CustomUser, id=user_id)
                  user.delete()
                  return redirect('users_list')
            else:
                  return redirect('users_list')




@never_cache
@resist_pages
@login_required
def user_detail_view(request,pk):
      user_details = get_object_or_404(CustomUser, pk=pk)
      if user_details.is_trainer==True:
            new_reg_user = CustomUser.objects.get(pk=pk,is_trainer=True)
            return render(request,'unapproved-user-view.html',{'new_reg_user': new_reg_user })
            
      elif user_details.is_student==True:
             new_reg_user = CustomUser.objects.get(pk=pk,is_student=True)
             return render(request,'unapproved-user-view.html',{'new_reg_user': new_reg_user })
      else:
         
           return render(request,'unapproved-user-view.html',)



@never_cache
@resist_pages
@login_required
def update_payment_status(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == "POST":
        is_paid_now = 'is_paid' in request.POST  # Directly check if 'is_paid' checkbox is checked
        
        if user.is_paid != is_paid_now:  # Check if the payment status has actually changed
            user.is_paid = is_paid_now
            user.save()
            if is_paid_now:
                messages.success(request, 'Payment received.')
            else:
                messages.success(request, 'User marked as not paid.')
        else:
            messages.info(request, 'No changes were made to the payment status.')
        
        return redirect('update_payment_status', pk=pk)  # Redirect to the appropriate URL

    context = {'new_reg_user': user}  
    return render(request, 'unapproved-user-view.html', context)



@never_cache
@resist_pages
@login_required
def student_details(request):
      student_users =StudentProfile.objects.all()
      return render(request,'student-details.html',{'student_users': student_users})


@never_cache
@resist_pages
@login_required     
def trainer_details(request):
      trainer_users =TrainerProfile.objects.all()
      return render(request,'trainer-detail.html',{'trainer_users':  trainer_users })
      

@never_cache
@resist_pages
@login_required
def operations(request):
       
      get_trainers = TrainerProfile.objects.all()
      get_students = StudentProfile.objects.all()
      context = {
            'get_trainers': get_trainers,
            'get_students': get_students
      }
      return render(request,'operations.html',context)


@never_cache
@resist_pages
@login_required
def assign_trainers(request,pk):
      if request.method == 'POST':
           assigned_trainer_id = request.POST.get('trainer')
           assign_trainer = get_object_or_404(TrainerProfile, pk=assigned_trainer_id)

           student = get_object_or_404(StudentProfile, pk=pk)
           student.assigned_trainer.add(assign_trainer)
           assign_trainer.assigned_students.add(student)
           
           return redirect('operations')
          


@never_cache
@resist_pages
def user_enquiry(request):
     if request.method == 'POST':
          description = request.POST.get('description')
          name = request.POST.get('name')
          email = request.POST.get('email')
          subject = request.POST.get('subject')

          enquiry_obj = CustomerEnquiry.objects.create(description=description,name=name,email=email,subject=subject)
          if enquiry_obj:
               messages.success(request, 'Enquiry successfully created an executive willconatct you soon')
          return redirect('contact')
     else:
          
        return render(request,'contact.html',{'enquiry_obj':enquiry_obj})
          

@never_cache
@resist_pages
@login_required
def all_cus_enquiries(request):
     enquiry_data = CustomerEnquiry.objects.all()
     return render(request,'enquiry-details.html',{'enquiry_data':enquiry_data})



@never_cache
@resist_pages
@login_required
def online_payment_details(request):
     order_details = Order.objects.all()
     return render(request,'online-payment.html',{'user_order_details':order_details})