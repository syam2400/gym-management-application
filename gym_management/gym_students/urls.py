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
from gym_students import views

urlpatterns = [
    path("student_homepage/",views.students_homepage_view,name="student_homepage"),
    path('student_profile/', views.students_profile_view,name="student_profile"),
    path('edit-user-details/<int:pk>/', views.update_user_details,name="edit_user_details"),

    path("<str:slug>/", views.chat_rooms_view, name="chat_room_page"),

    path('initiate-payments', views.initiate_payment_view,name="initiate_payments"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
  
  
]

