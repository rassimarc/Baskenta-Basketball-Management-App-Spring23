from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
    usertype = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_book = models.CharField(max_length=30)
    favorite_food = models.CharField(max_length=30)
    favorite_holiday = models.CharField(max_length=30)
    favorite_fictional_character = models.CharField(max_length=30)

