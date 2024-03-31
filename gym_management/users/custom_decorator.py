
from functools import wraps

from django.shortcuts import get_object_or_404, redirect
from django.urls import resolve
from users.models import CustomUser

'''
decorator for resisting the user's movment towards previous common pages that if he is not logged out.
users can only see their on perosonal pages,not other users pages and common pages.  
     
'''
def resist_pages(func):
    studentuser_urls = ['student_homepage','student_profile' ,'edit_user_details','chat_room_page','initiate_payments',
                        'payment-success','payment_failed','payment_details','contact']
    trainer_user_urls = ['trainer_homepage','trainer_profile','trainer_details','chat_room','contact']

    owner_urls = ['users_list','approve_user','user_details','update_payment_status','student_details',
                  'trainer_details','operations','assign_trainers','enquiry','view_enquiry_data','online_payment','contact']
    
    @wraps(func)
    def wrapper(request,*args, **kwargs):
        if request.session.get('user_key'):
                logged_user = get_object_or_404(CustomUser,username=request.session.get('user_key'))   
                current_view_name = resolve(request.path_info).url_name 
                if logged_user.is_trainer :            
                      if current_view_name in  trainer_user_urls :
                         return func(request, *args, **kwargs)
                      else:
                          return redirect('trainer_homepage')
                elif logged_user.is_student :
                    if current_view_name in studentuser_urls:
                         return func(request, *args, **kwargs)     
                    else:
                          return redirect('student_homepage')
                elif logged_user.is_superuser:
                    if current_view_name in  owner_urls:
                         return func(request, *args, **kwargs)    
                    else:
                          return redirect('users_list')                           
                else:
                       return True
        else:
              return func(request, *args, **kwargs)
    
    return wrapper