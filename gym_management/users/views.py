from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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

        user = CustomUser.objects.create(username=username, email=email, phone=phone,
                                             age=age, place= place,gender=gender, fitness_level=fitness_level,goal=goal)
        
        user. is_student = True
        user.set_password(password)

        user.save()
        return redirect('user_login')
    
    return render(request,"student_signup.html")


def trainer_registeration_form(request):
       
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST['email']
        phone = request.POST["phone"]
        age = request.POST["age"]
        place = request.POST["place"]
        gender = request.POST["gender"]
        specialization = request.POST["special"]
        experience_years = request.POST["exp-yrs"]
        certifications = request.POST["cert"]
        qualification = request.POST["qualif"]

        password = request.POST.get("password")

        user = CustomUser.objects.create(username= username ,email=email, phone=phone,age=age, place=place,gender=gender, 
                                             specialization=specialization, experience_years= experience_years,
                                              certifications= certifications,qualification=qualification)
        
        user.is_trainer = True
        user.set_password(password)

        user.save()
        return redirect('user_login')


    return render(request,"trainer_signup.html")



@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
            
        if user is not None :
            if user.is_approved :
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
                return HttpResponseForbidden("Your account is pending approval by the admin.")
        else:
                return HttpResponseForbidden("Invalid login credentials.")
    else:
        return render(request,'user_login.html')
    
    
def user_logout(request):
    logout(request)
    return  user_login(request)
