from django.shortcuts import render

def students_homepage(request):
    return render(request,"students-index.html")
