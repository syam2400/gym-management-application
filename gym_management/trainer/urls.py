"""
URL configuration for gym_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from trainer import views

urlpatterns = [
  
    path('trainer-homepage',views.trainer_homepage,name='trainer_homepage'),
    path('trainer_profile/', views.trainer_profile_view,name="trainer_profile"),
    path('trainer_details/<int:pk>/', views.update_trainer_details,name="trainer_details"),
    path("<str:slug>/", views.chat_room, name="chat_room")
   
]

