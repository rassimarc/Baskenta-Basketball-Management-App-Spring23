from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from app1.models import *
from .forms import *
from django.contrib import messages



def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'aboutus.html')
        


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
        return render(request, 'management_manager.html', {'teams':teams, 'signup_requests':Request.objects.all()})

        

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
                if not user.profile.accepted:
                    return redirect("not_accepted")
                login(request, user)
                return redirect('myuser')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def performance(request):
    stats=Stats.objects.all()
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'performance.html',{'stats':stats})
        
def signup_player(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the user's information to the database
            user = form.save()
            profile = Profile.objects.create(usertype="Player",user=user,favorite_book=form.cleaned_data.get('favorite_book'),favorite_food=form.cleaned_data.get('favorite_food'),favorite_holiday=form.cleaned_data.get('favorite_holiday'),due_payment=0,accepted=False,monthly_payment=0)
            user.profile.save()
            request = Request.objects.create(player=user)
            request.save()
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
            Profile.objects.create(usertype="Coach",user=user,favorite_book=form.cleaned_data.get('favorite_book'),favorite_food=form.cleaned_data.get('favorite_food'),favorite_holiday=form.cleaned_data.get('favorite_holiday'),due_payment=0,accepted=True,monthly_payment=0)
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
            Profile.objects.create(usertype="Manager",user=user,favorite_book=form.cleaned_data.get('favorite_book'),favorite_food=form.cleaned_data.get('favorite_food'),favorite_holiday=form.cleaned_data.get('favorite_holiday'),due_payment=0,accepted=True, monthly_payment=0)
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
        	



from django.http import JsonResponse 
  

def schedule(request):
    if not request.user.is_authenticated:
        return redirect("login")
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'schedule.html',context)
 
def all_events(request):                                                                                               
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
            'description': event.description,                                                           
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
         
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    description = request.GET.get("description", None)
    event = Events(name=str(title), start=start, end=end, description=description)
    event.save()
    data = {}
    return JsonResponse(data)
 
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    description = request.GET.get("description", None) # Get the description field value
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.description = description # Update the description field
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)
def add_stat(request):
    submitted = False
    if request.method == "POST":
        form = PlayerStat(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Stats.objects.filter(name=name).exists():
                form.add_error('name', 'Statistics for this player have already been recorded')
            else:
                form.save()
                return redirect('performance')    
    else:
        form = PlayerStat()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_stat.html', {'form': form, 'submitted': submitted})

def update_stat(request, stats_name):
    stats = Stats.objects.get(name=stats_name)
    form = PlayerStat(request.POST or None, request.FILES or None, instance=stats)
    if form.is_valid():
        form.save()
        return redirect('performance')
    return render(request, 'update_stat.html', {'stats': stats, 'form': form})

def payment(request):
    player_name = request.user.get_full_name() # Get the player's name
    remaining_amount = request.user.profile.due_payment # Get the remaining amount
    if request.method == 'POST':
        # Handle form submission
        amount_paid = int(request.POST.get('amount_paid'))
        remaining_amount -= amount_paid
        request.user.profile.due_payment=remaining_amount
        request.user.profile.save()
    else:
        amount_paid = None
    context = {
        'player_name': player_name,
        'remaining_amount': remaining_amount,
        'amount_paid': amount_paid
    }
    return render(request, 'payment.html', context)


def not_accepted(request):
    return render(request, 'not_accepted.html')
def reject_request(request, username):
    user = User.objects.get(username=username)
    request = Request.objects.get(player=user)
    request.delete()
    user.delete()
    return redirect("management")

def accept_request(request, username):
    user = User.objects.get(username=username)
    signup_request = Request.objects.get(player=user)
    due_amount = request.POST.get('due_amount')  # get the due_amount value from the POST request
    signup_request.delete()
    user.profile.accepted = True
    user.profile.due_payment = due_amount  # set the due_payment value to the due_amount value
    user.profile.monthly_payment = due_amount  # set the monthly_payment value to the due_amount value
    user.profile.save()
    return redirect("management")

def player_profile(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    return render(request, 'player_profile.html', {'user': user, 'profile': profile})

def all_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'all_members.html', {'profiles': profiles})

