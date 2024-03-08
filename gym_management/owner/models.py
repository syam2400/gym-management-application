from django.db import models

class CustomerEnquiry(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    subject = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
