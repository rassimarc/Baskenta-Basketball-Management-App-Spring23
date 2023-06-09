from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import *


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    age = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)
    position = forms.CharField(required=False)
    favorite_book = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_food = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_holiday = forms.CharField(max_length=30, required=True, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'favorite_book', 'favorite_food', 'favorite_holiday', 'age', 'height', 'weight', 'position')

class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, help_text="Required")
    new_password = forms.CharField(max_length=30, widget = forms.PasswordInput(), required=True, help_text="Required")
    favorite_book = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_food = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_holiday = forms.CharField(max_length=30, required=True, help_text='Required')

# Admin SuperUser Event Form
class TeamFormAdmin(ModelForm):
	class Meta:
		model = Team
		fields = ('name', 'coach', 'players')
		labels = {
			'name': '',
			'coach': 'Coach',
			'players': 'Players',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team Name'}),
			'coach': forms.Select(attrs={'class':'form-select', 'placeholder':'Coach'}),
			'players': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Players'}),
		}

# Edit Personal Info Form

class UserUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

        

class PlayerStat(ModelForm):
    class Meta:
        model = Stats
        fields = ('name', 'position', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TOVPG', 'MPG', 'rating')
        labels = {
            'name': 'name',
            'position': ' ',
            'PPG': ' ',
            'RPG': ' ',
            'APG': ' ',
            'SPG': ' ',
            'BPG': ' ',
            'TOVPG': ' ',
            'MPG': ' ',
            'rating': ' ',
        }
        widgets = {
            'name': forms.Select(attrs={'class': 'form-select', 'placeholder': 'name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'PPG': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PPG'}),
            'RPG': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'RPG'}),
            'APG': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'APG'}),
            'SPG': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'SPG'}),
            'BPG': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'BPG'}),
            'TOVPG': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'TOVPG'}),
            'MPG': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MPG'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rating', 'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        ppg = cleaned_data.get('PPG')
        rpg = cleaned_data.get('RPG')
        apg = cleaned_data.get('APG')
        spg = cleaned_data.get('SPG')
        bpg = cleaned_data.get('BPG')
        tovpg = cleaned_data.get('TOVPG')
        mpg = cleaned_data.get('MPG')
        rating = (ppg*2.5) + (rpg*2.0) + (apg*1.5) + (spg * 1.0) + (bpg * 1.0) - (tovpg * 1.5) + (mpg * 0.5)
        cleaned_data['rating'] = rating
        return cleaned_data



class SignupRequestForm(forms.Form):
    due_amount = forms.IntegerField(label='Due amount')
    
class FinancialAidForm(forms.Form):
    player_name = forms.CharField(label="Full Name", max_length=100)
    player_username = forms.CharField(label="Username", max_length=100)
    player_age = forms.IntegerField(label="Age", min_value=1, max_value=99)
    player_email = forms.EmailField(label="Email")
    annual_income = forms.IntegerField(label="Annual Income", min_value=1, max_value=100000000)
    family_size = forms.IntegerField(label="Family Size", min_value=1, max_value=20)
    reason = forms.CharField(label="Reason for Financial Aid", widget=forms.Textarea(attrs={"rows": 5, "cols": 30}))
    
# the following form is for the manager to accept or reject a player's request, and to enter the percentage of financial aid to be given:
# class AcceptAidRequestForm(forms.Form):
#     percentage = forms.IntegerField(label="Percentage of Financial Aid", min_value=0, max_value=100)
#     is_accepted = forms.ChoiceField(choices=[(True, 'Accept'), (False, 'Decline')], widget=forms.RadioSelect)

#     class Meta:
#         model = User
#         fields = ('percentage', 'is_accepted')
class AcceptAidRequestForm(forms.Form):
    percent_aid = forms.IntegerField(min_value=0, max_value=100, required=True)


class GameStat(ModelForm):
	class Meta:
		model = Games
		fields = ('Team1', 'Team2', 'Winner')
		labels = {
			'Team1': 'Team1',
			'Team2': 'Team2',
			'Winner': ' ',
		}
		widgets = {
			'Team1': forms.Select(attrs={'class':'form-select', 'placeholder':'Team1'}),
			'Team2': forms.Select(attrs={'class':'form-select', 'placeholder':'Team2'}),
            'Winner': forms.Select(attrs={'class':'form-select', 'placeholder':'Winner'}),
		}
     