from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
    usertype = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_book = models.CharField(max_length=30)
    favorite_food = models.CharField(max_length=30)
    favorite_holiday = models.CharField(max_length=30)
    favorite_fictional_character = models.CharField(max_length=30)
    def __str__(self):
        return self.user.username

class Team(models.Model):
    name = models.CharField('Event Name', max_length=120)
    coach = models.ForeignKey(Profile, related_name='coached_teams', limit_choices_to={'usertype': 'Player'}, blank=True, null=True, on_delete=models.SET_NULL)
    players = models.ManyToManyField(Profile, related_name='played_teams', limit_choices_to={'usertype': 'Player'}, blank=True)
	
    def __str__(self):
        return self.name