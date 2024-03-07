from django.db import models

from users.models import CustomUser


class TrainerProfile(models.Model):
    trainer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    trainer_bio = models.TextField(null=True, blank=True)
    trainer_profile_picture = models.ImageField(upload_to='media/profile_pictures/', null=True, blank=True)
    assigned_students = models.ManyToManyField('gym_students.StudentProfile', blank=True)
    

    def __str__(self):
        return self.trainer.username
      
    