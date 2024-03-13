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
from users import views

urlpatterns = [
  
    path('',views.home,name='home'),
    path('contact-page',views.contact_page,name='contact'),
    path('blog/',views.blog_page,name='blog'),
    path('blog-elements/',views.blog_elements_page,name='blog_elements'),
    path('gallery/',views.gallery_page,name='gallery'),
    path('pricing_page',views.pricing_page,name='pricing'),
    path('courses/',views.courses_page,name='courses'),
    path('about/',views.about_page,name='about'),


    path('register', views.registration_redirection,name='register'), #connects to a common registration button
    path('trainer_register', views.trainer_registeration_form,name='trainer_register'),
    path('student_register', views.student_registeration_form,name='student_register'),
    # path("decline",views.decline,name="decline")

    path('user_login',views.user_login,name='user_login'),
    path('logout/', views.user_logout, name='logout')
]

