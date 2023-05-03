from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
    usertype = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=30, blank=True, null=True)
    favorite_book = models.CharField(max_length=30)
    favorite_food = models.CharField(max_length=30)
    favorite_holiday = models.CharField(max_length=30)
    due_payment = models.IntegerField(blank=True, null=True)
    accepted = models.BooleanField()
    monthly_payment = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.user.username

class Team(models.Model):
    name = models.CharField('Event Name', max_length=120)
    coach = models.ForeignKey(Profile, related_name='coached_teams', limit_choices_to={'usertype': 'Coach'}, blank=True, null=True, on_delete=models.SET_NULL)
    players = models.ManyToManyField(Profile, related_name='played_teams', limit_choices_to={'usertype': 'Player'}, blank=True)
	
    def __str__(self):
        return self.name

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Stats(models.Model):
    name = models.ForeignKey(Profile, related_name='players', limit_choices_to={'usertype': 'Player'}, blank=True, null=True, on_delete=models.SET_NULL)
    position = models.CharField('Position', max_length=120)
    stat1 = models.CharField('stat1', max_length=120)

    def __str__(self):
        return self.name

class Request(models.Model):
    player =  models.ForeignKey(User, on_delete=models.CASCADE)


class FinancialAid(models.Model):
    player_name = models.CharField(max_length=100, blank=True, null=True)
    player_username = models.CharField(max_length=100, blank=True, null=True)
    player_age = models.IntegerField(blank=True, null=True)
    player_email = models.EmailField(blank=True, null=True)
    annual_income = models.IntegerField(blank=True, null=True)
    family_size = models.IntegerField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, default="Pending")

    def __str__(self):
        return f"{self.player_name} - Requested Financial Aid"

