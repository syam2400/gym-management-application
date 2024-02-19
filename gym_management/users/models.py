from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    GOALS = [
        ('LOSE','Weight lose'),
        ('FIT','Maintain weight'),
        ('GAIN','Weight gain'),
    ]
    FITNESS_LEVEL = [
        ('Beginner','Beginner'),
        ('Intemediate','Intemediate'),
        ('Advanced','Advanced')
    ]
    age = models.IntegerField(default=0,null=True,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True,blank=True)
    phone = models.PositiveIntegerField(default=0,null=True, blank=True)
    place = models.CharField(max_length=30,null=True,blank=True)

    #this fields is for trianers registration  
    bio = models.TextField(null=True, blank=True)
    specialization = models.CharField(max_length=30,null=True,blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    certifications = models.CharField(max_length=50,null=True, blank=True)
    qualification = models.CharField(max_length=30,null=True,blank=True)

    #below fields are for gym students
    goal = models.CharField(max_length=10,choices=GOALS,null=True, blank=True)
    fitness_level = models.CharField(max_length=15,choices=FITNESS_LEVEL, null=True, blank=True)

    is_approved= models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
 
    
    def __str__(self):
        return self.username
    
    
