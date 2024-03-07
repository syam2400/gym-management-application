from django.db import models

from users.models import CustomUser



class StudentProfile(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    student_bio = models.TextField(null=True, blank=True)
    student_profile_picture = models.ImageField(upload_to='media/profile_pictures/', null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    assigned_trainer = models.ManyToManyField('trainer.TrainerProfile', blank=True)

    
    def __str__(self):
        return self.student.username



