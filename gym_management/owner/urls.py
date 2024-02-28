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
from owner import views

urlpatterns = [
  
    path('users-list',views.users_list,name='users_list'),
    path('approve-user/<int:user_id>/',views.approve_user,name='approve_user'),
    path('student_details',views.student_details,name='student_details'),
    path('trainer_details',views.trainer_details,name='trainer_details'),
    path('operations',views.operations,name='operations'),
]

