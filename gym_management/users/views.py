from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request,'index.html')

def contact_page(request):
     return render(request,'contact.html')

def blog_page(request):
     return render(request,'blog.html')

def blog_elements_page(request):
     return render(request,'blog-elements.html')

def gallery_page(request):
     return render(request,'gallery.html')

def pricing_page(request):
     return render(request,'pricing.html')

def courses_page(request):
     return render(request,'courses.html')

def about_page(request):
     return render(request,'about.html')


# when signup button clicks it will redirect to user registeration button page
def registration_redirection(request):
    return render(request,"register.html")

        


def student_registeration_form(request):   
   if request.method == "POST":

        username = request.POST["username"]
        email = request.POST['email']
        phone = request.POST["phone"]
        age = request.POST["age"]
        place = request.POST["place"]
        gender = request.POST["gender"]
        fitness_level = request.POST["fitness_level"]
        goal = request.POST["goal"]

        password = request.POST["password"] 

        try:
            # Attempt to create a new user
            user = CustomUser.objects.create(username=username, email=email, phone=phone,
                                                age=age, place=place, gender=gender, fitness_level=fitness_level, goal=goal)
            user.is_student = True
            user.set_password(password)
            user.save()
            return redirect('user_login')
        
        except IntegrityError:
            # Handle the case where the username already exists
            message = "Username already exists. Please choose a different one."
            return render(request, 'student_signup.html', {'message': message})

        except Exception as e:
            # Handle any other exceptions here
            print(e)  # Print the exception for debugging purposes
            message = "An error occurred. Please try again later."
            return render(request, 'student_signup.html', {'message': message})

   return render(request, 'student_signup.html')


def trainer_registeration_form(request):
       
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST['email']
        phone = request.POST["phone"]
        age = request.POST["age"]
        place = request.POST["place"]
        gender = request.POST["gender"]
        specialization = request.POST.get('special')
        experience_years = request.POST["exp-yrs"]
        certifications = request.POST["cert"]
        qualification = request.POST["qualif"]

        password = request.POST.get("password")


        try:
            user = CustomUser.objects.create(username=username,email=email, phone=phone,age=age, place=place,gender=gender, 
                                             specialization=specialization, experience_years= experience_years,
                                              certifications= certifications,qualification=qualification)
            user.is_student = True
            user.set_password(password)
            user.save()
            return redirect('user_login')
        
        except IntegrityError:
            # Handle the case where the username already exists
            message = "Username already exists. Please choose a different one."
            return render(request, 'trainer_signup.html', {'message': message})

        except Exception as e:
            # Handle any other exceptions here
            print(e)  # Print the exception for debugging purposes
            message = "An error occurred. Please try again later."
            return render(request, 'trainer_signup.html', {'message': message})

    return render(request,"trainer_signup.html")


def social_user_login(request):
     social_user = get_object_or_404(CustomUser,username=request.user)
     if social_user.is_student == True and social_user.is_approved == True :
           return redirect('student_homepage')
     
     elif social_user.is_trainer == True and social_user.is_approved == True :
           return redirect('trainer_homepage')
     elif social_user.is_trainer or social_user.is_student :
          message = "login request is pending , you can login if the admin gives the approval"
          return render(request, 'social-auth.html',{'message': message})
 
     else :
          if request.method == 'POST':
               role = request.POST.get('role')
               if role == 'trainer':
                    social_user.is_trainer = True
                    social_user.save()
                    return redirect('user_login')
               else :
                    social_user.is_student = True
                    social_user.save()
                    return redirect('user_login')
    
     return render(request,'social-auth.html')


@never_cache
def user_login(request):
       
        if request.session.get('user_key'):
                print(request.session.get('user_key'))
                logged_user = get_object_or_404(CustomUser,username=request.session.get('user_key'))
                print("hiiii",logged_user)
                if logged_user.is_trainer :
                    return redirect('trainer_homepage')
                elif logged_user.is_student :
                        return redirect('student_homepage')
                # elif logged_user.is_superuser:
                else:
                       return redirect('users_list')
                # else:
                #       return render(request,'user_login.html')
        else:
                         
                if request.method == "POST":
                    username = request.POST.get('username')
                    password = request.POST.get('password')

                    user = authenticate(username=username,password=password)
                   
                        
                    if user is not None :
                        if user.is_approved :
                                request.session['user_key'] = username
                                if user.is_student :
                                    login(request, user)
                                    return redirect('student_homepage')
                                elif user.is_trainer :
                                    login(request, user)
                                    return redirect('trainer_homepage')
                                elif user.is_superuser :
                                    login(request, user)
                                    return redirect('users_list')
                                else :
                                    error_messages = "invalid credentials"
                                    return render(request, 'user_login.html', {'error_messages':  error_messages})
                                    
                        else:
                            return render(request,"decline.html")
                    else:
                            return HttpResponseForbidden("Invalid login credentials.")
                else:
                    return render(request,'user_login.html')
                
        
def user_logout(request):
   
    logout(request)
    if 'user_key' in request.session:
        print("hlo",request.session.get('user_key'))
        del request.session['user_key']
    return  redirect("user_login")
