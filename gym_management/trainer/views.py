from django.shortcuts import render,redirect

# def trainer_homepage(request):
#     return render(request,'trainer-index.html')

def loginRegisterPage(request):
    return render(request,"loginRegister.html")
    
