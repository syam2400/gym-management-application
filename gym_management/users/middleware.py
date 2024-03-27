from django.shortcuts import get_object_or_404, redirect

from users.models import CustomUser

class CheckSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
       
                
        # if not request.session.get('user_key') and request.path != 'user_login':
        #     return redirect('user_login')


        response = self.get_response(request)
        if request.session.get('user_key'):
                print(request.session.get('user_key'))
                logged_user = get_object_or_404(CustomUser,username=request.session.get('user_key'))
                print("hiiii",logged_user)
                if logged_user.is_trainer :
                    return redirect('trainer_homepage')
                elif logged_user.is_student and  request.path != 'student_homepage/' or request.path != 'student_profile/' or request.path != 'edit-user-details/<int:pk>/':
                        return redirect('student_homepage')
                # elif logged_user.is_superuser:
                else:
                       return redirect('users_list')

        # Code to be executed for each request/response after
        # the view is called.

        return response
