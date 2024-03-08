from django.shortcuts import get_object_or_404, redirect, render
from users.models import *
from trainer.models import *
from gym_students.models import *
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from owner.models import *


def users_list(request):
    trainer_users = CustomUser.objects.filter(is_trainer=True)
    student_user = CustomUser.objects.filter(is_student=True)
    context = {
         'trainer_users': trainer_users,
         'student_users':student_user
    }
    return render(request,'owner-index.html',context)

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


def user_detail_view(request,pk):
      user_details = get_object_or_404(CustomUser, pk=pk)
      if user_details.is_trainer==True:
            new_reg_user = CustomUser.objects.get(pk=pk,is_trainer=True)

      elif user_details.is_student==True:
             new_reg_user = CustomUser.objects.get(pk=pk,is_student=True)
      else:
           new_reg_user = None 
      return render(request,'unapproved-user-view.html',{'new_reg_user': new_reg_user })

# def update_payment_status(request,pk):
#       update_user_payment = get_object_or_404(CustomUser,pk=pk)
#       # update_user_payment.is_paid = True
#       # update_user_payment.save()
#       if 'payment_status_submitted' in request.POST:
#         update_user_payment.is_paid = 'is_paid' in request.POST
#         update_user_payment.save()
#         context = {'status': 'payement received'}
#         return render(request,'unapproved-user-view.html', context)
#       return render(request,'unapproved-user-view.html')

def update_payment_status(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == "POST":
        if 'payment_status_submitted' in request.POST:
            is_paid_now = 'is_paid' in request.POST
            # Check if there's an attempt to change the status
            if user.is_paid and not is_paid_now:
                # User was paid, now marking as unpaid
                user.is_paid = False
                user.save()
                messages.success(request, 'User marked as not paid.')
            elif not user.is_paid and is_paid_now:
                # User was not paid, now marking as paid
                user.is_paid = True
                user.save()
                messages.success(request, 'Payment received.')
            else:
                # No change in status, provide appropriate feedback
                messages.info(request, 'No changes were made to the payment status.')
            
            # Redirect to avoid post-redirect-get pattern issues
            return redirect('update_payment_status', pk=pk)
    # For GET requests or if 'payment_status_submitted' is not in POST data
    context = {'new_reg_user': user}  # Assuming 'new_reg_user' is expected in the template
    return render(request, 'unapproved-user-view.html', context)



def student_details(request):
      student_users =StudentProfile.objects.all()

      return render(request,'student-details.html',{'student_users': student_users})
      
def trainer_details(request):
      trainer_users =TrainerProfile.objects.all()
      # assigned_students = trainer_users.assigned_students
      return render(request,'trainer-detail.html',{'trainer_users':  trainer_users })
      

def operations(request):
       
      get_trainers = TrainerProfile.objects.all()
      get_students = StudentProfile.objects.all()
      context = {
            'get_trainers': get_trainers,
            'get_students': get_students
      }
      return render(request,'operations.html',context)

def assign_trainers(request,pk):
      if request.method == 'POST':
           assigned_trainer_id = request.POST.get('trainer')
           assign_trainer = get_object_or_404(TrainerProfile, pk=assigned_trainer_id)

           student = get_object_or_404(StudentProfile, pk=pk)
           student.assigned_trainer.add(assign_trainer)
           assign_trainer.assigned_students.add(student)
           
           return redirect('operations')
          

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
          

def all_cus_enquiries(request):
     enquiry_data = CustomerEnquiry.objects.all()
     return render(request,'enquiry-details.html',{'enquiry_data':enquiry_data})