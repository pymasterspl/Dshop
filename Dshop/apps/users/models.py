from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    shipping_address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return str(self.user)