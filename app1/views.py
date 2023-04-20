from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from app1.models import *
from .forms import *
from django.contrib import messages



def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'home.html')

def aboutus(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'aboutus.html')
        
def schedule(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'schedule.html')

def communication(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'communication.html')

def management(request):
    teams=Team.objects.all()	
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.profile.usertype == "Player":
        return render(request, 'management_player.html', {'teams':teams})
    if request.user.profile.usertype == "Coach":
        return render(request, 'management_coach.html', {'teams':teams})
    if request.user.profile.usertype == "Manager":
        return render(request, 'management_manager.html', {'teams':teams})

        

def logout_view(request):
    logout(request)
    return redirect('login')

def change_password(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["new_password1"])
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect("myuser")
    form = PasswordChangeForm(request.user)
    return render(request, 'changePassword.html', {'form': form})

def myuser(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'myuser.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('myuser')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def performance(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'performance.html')
        
def signup_player(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the user's information to the database
            user = form.save()
            profile = Profile.objects.create(usertype="Player",user=user,favorite_book=form.cleaned_data.get('favorite_book'),favorite_food=form.cleaned_data.get('favorite_food'),favorite_holiday=form.cleaned_data.get('favorite_holiday'),favorite_fictional_character=form.cleaned_data.get('favorite_fictional_character'))
            user.profile.save()
            # Redirect the user to the login page
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup_player.html', {'form': form})


def signup_coach(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the user's information to the database
            user = form.save()
            Profile.objects.create(usertype="Coach",user=user,favorite_book=form.cleaned_data.get('favorite_book'),favorite_food=form.cleaned_data.get('favorite_food'),favorite_holiday=form.cleaned_data.get('favorite_holiday'),favorite_fictional_character=form.cleaned_data.get('favorite_fictional_character'))
            user.profile.save()

            # Redirect the user to the login page
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup_coach.html', {'form': form})

def signup_manager(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the user's information to the database
            user = form.save()
            Profile.objects.create(usertype="Manager",user=user,favorite_book=form.cleaned_data.get('favorite_book'),favorite_food=form.cleaned_data.get('favorite_food'),favorite_holiday=form.cleaned_data.get('favorite_holiday'),favorite_fictional_character=form.cleaned_data.get('favorite_fictional_character'))
            user.profile.save()

            # Redirect the user to the login page
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup_manager.html', {'form': form})

def delete_account(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        if request.POST.get("confirm") == "yes":
            request.user.profile.delete()
            request.user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect("login")
        else:
            return redirect("myuser") 

    return render(request, 'confirm_delete_account.html')

def forgot_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            new_password = form.cleaned_data.get('new_password')
            user = User.objects.get(username=username)
            if user is not None:
                if user.profile.favorite_book == form.cleaned_data.get('favorite_book') and user.profile.favorite_food == form.cleaned_data.get('favorite_food') and user.profile.favorite_holiday == form.cleaned_data.get('favorite_holiday') and user.profile.favorite_fictional_character == form.cleaned_data.get('favorite_fictional_character'):
                    user.set_password(new_password)
                    user.save()
                    return redirect("login")
    else:
        form = ResetPasswordForm()
    return render(request, 'forgotpassword.html', {'form': form})

from django.shortcuts import get_object_or_404
from django.http import Http404

def add_team(request):
    submitted = False
    if request.method == "POST":
        form = TeamFormAdmin(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Team.objects.filter(name=name).exists():
                form.add_error('name', 'A team with this name already exists.')
            else:
                form.save()
                return redirect('management')    
    else:
        form = TeamFormAdmin()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_team.html', {'form': form, 'submitted': submitted})

def update_team(request, team_name):
	team = Team.objects.get(name=team_name)
	form = TeamFormAdmin(request.POST or None, request.FILES or None, instance=team)
	if form.is_valid():
		form.save()
		return redirect('management')
	return render(request, 'update_team.html', 
		{'team': team,
		'form':form})

def delete_team(request,team_name):
    if request.method == "POST":
        if request.POST.get("confirm") == "yes":
            team = Team.objects.get(name=team_name)
            team.delete()
            return redirect('management')
        else:
            return redirect("management")    

    return render(request, 'confirm_delete_team.html')	
        

def Edit_Personal_Info(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myuser')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'Edit_Personal_Info.html', {'form': form})
        	