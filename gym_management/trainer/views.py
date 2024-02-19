from django.shortcuts import render

def trainer_homepage(request):
    return render(request,'trainer-index.html')
    
