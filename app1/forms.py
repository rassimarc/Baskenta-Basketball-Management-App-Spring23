from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import Team


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_book = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_food = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_holiday = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_fictional_character = forms.CharField(max_length=30, required=True, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'favorite_book', 'favorite_food', 'favorite_holiday', 'favorite_fictional_character')

class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, help_text="Required")
    new_password = forms.CharField(max_length=30, widget = forms.PasswordInput(), required=True, help_text="Required")
    favorite_book = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_food = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_holiday = forms.CharField(max_length=30, required=True, help_text='Required')
    favorite_fictional_character = forms.CharField(max_length=30, required=True, help_text='Required')

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