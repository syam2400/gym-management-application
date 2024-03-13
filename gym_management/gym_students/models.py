from django.db import models

from users.models import CustomUser



class StudentProfile(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    student_bio = models.TextField(null=True, blank=True)
    student_profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    assigned_trainer = models.ManyToManyField('trainer.TrainerProfile', blank=True)

    
    def __str__(self):
        return self.student.username




class Room(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=100)


    def __str__(self):
        return "Room : "+ self.name + " | Id : " + self.slug
    

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "Message is :- "+ self.content