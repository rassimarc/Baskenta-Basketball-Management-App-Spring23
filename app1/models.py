from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
    usertype = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
