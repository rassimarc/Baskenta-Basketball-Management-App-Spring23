from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from app1.models import *
from .forms import *
from django.contrib import messages
from chat.models import *
from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import Http404

def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'aboutus.html')
        
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
    games=Games.objects.all()
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.profile.usertype == "Player":
        return render(request, 'performance_player.html', {'stats':stats, 'games':games})
    if request.user.profile.usertype == "Coach":
        return render(request, 'performance_coach.html', {'stats':stats,'games':games})
    if request.user.profile.usertype == "Manager":
        return render(request, 'performance_manager.html', {'stats':stats,'games':games})
        
def signup_player(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the user's information to the database
            user = form.save()
            profile = Profile.objects.create(usertype="Player",user=user,favorite_book=form.cleaned_data.get('favorite_book'),favorite_food=form.cleaned_data.get('favorite_food'),favorite_holiday=form.cleaned_data.get('favorite_holiday'),due_payment=0,accepted=False,monthly_payment=0, age=form.cleaned_data.get('age'), height=form.cleaned_data.get('height'), weight=form.cleaned_data.get('weight'), position=form.cleaned_data.get('position') )
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
        if request.POST.get("confirm") == "yes" and request.user.profile.due_payment == 0:
            request.user.profile.delete()
            request.user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect("login")
        elif request.POST.get("confirm") == "yes" and request.user.profile.due_payment != 0:
            messages.success(request,"You cannot delete your account because you have a due payment")
            return redirect('myuser')
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
                if user.profile.favorite_book == form.cleaned_data.get('favorite_book') and user.profile.favorite_food == form.cleaned_data.get('favorite_food') and user.profile.favorite_holiday == form.cleaned_data.get('favorite_holiday'):
                    user.set_password(new_password)
                    user.save()
                    return redirect("login")
    else:
        form = ResetPasswordForm()
    return render(request, 'forgotpassword.html', {'form': form})


def add_team(request):
    submitted = False
    if request.method == "POST":
        form = TeamFormAdmin(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Team.objects.filter(name=name).exists():
                form.add_error('name', 'A team with this name already exists.')
            else:
                if not Room.objects.filter(name=room).exists():
                    new_room = Room.objects.create(name=name)
                    new_room.save()
                    
                form.save()
                return redirect('management')    
    else:
        form = TeamFormAdmin()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_team.html', {'form': form, 'submitted': submitted})

def update_team(request, team_name):
    room = get_object_or_404(Room, name=team_name)
    team = Team.objects.get(name=team_name)
    form = TeamFormAdmin(request.POST or None, request.FILES or None, instance=team)
    if form.is_valid():
        team = form.save(commit=False)
        room.name = team.name
        room.save()
        form.save()
        return redirect('management')
    
    return render(request, 'update_team.html', {'team':team, 'form':form})

def delete_team(request,team_name):
    if request.method == "POST":
        if request.POST.get("confirm") == "yes":
            team = Team.objects.get(name=team_name)
            room = Room.objects.get(name=team_name)
            team.delete()
            room.delete()
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

def update_stat(request, stats_id):
    stats = Stats.objects.get(id=stats_id)
    form = PlayerStat(request.POST or None, request.FILES or None, instance=stats)
    if form.is_valid():
        form.save()
        return redirect('performance')
    return render(request, 'update_stat.html', {'stats': stats, 'form': form})

def delete_stat(request, stats_id):
    if request.method == "POST":
        if request.POST.get("confirm") == "yes":
            stats = Stats.objects.get(id=stats_id)
            stats.delete()
            return redirect('performance')
        else:
            return redirect("performance")    

    return render(request, 'confirm_delete_stat.html')

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


# Create your views here.
def chat_home(request):
    teams=Team.objects.all()
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'chat_home.html', {'teams':teams})

def room(request, room):
    username = request.user.get_full_name()
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.user.get_full_name()
    return redirect(room+'/?username='+username) 
    
def send(request):
    message = request.POST['message']
    username = request.user.get_full_name()
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
def player_profile(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    return render(request, 'player_profile.html', {'user': user, 'profile': profile})

def all_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'all_members.html', {'profiles': profiles})

def all_players(request):
    profiles = Profile.objects.all()
    return render(request, 'all_players.html', {'profiles': profiles})

def player_profile_ForCoach(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    return render(request, 'player_profile_ForCoach.html', {'user': user, 'profile': profile})

def end_of_month(request):
    profile = Profile.objects.all()
    for player in profile:
        player.due_payment += player.monthly_payment
        player.save()
   #messages.success(request, 'Monthly payment added')
    return redirect('management')

from django.shortcuts import render, redirect
from .forms import FinancialAidForm

def financial_aid(request):
    if request.method == 'POST':
        form = FinancialAidForm(request.POST)
        if form.is_valid():
            # Save the form data to the database or do something else with it
            player_name = form.cleaned_data['player_name']
            player_username = form.cleaned_data['player_username']
            player_age = form.cleaned_data['player_age']
            player_email = form.cleaned_data['player_email']
            annual_income = form.cleaned_data['annual_income']
            family_size = form.cleaned_data['family_size']
            reason = form.cleaned_data['reason']
            
            financial_aid = FinancialAid(player_name=player_name,player_username=player_username, player_age=player_age, player_email=player_email, annual_income=annual_income, family_size=family_size, reason=reason)
            financial_aid.save()
            return redirect('financial_aid')
    else:
        form = FinancialAidForm()
    return render(request, 'financial_aid.html', {'form': form})


def aid_requests(request):
    profiles = Profile.objects.all()
    aid_requests = FinancialAid.objects.all()
    return render(request, 'aid_requests.html', {'aid_requests': aid_requests, 'profiles': profiles})

def accept_aid_request(request, request_id):
    aid_request = get_object_or_404(FinancialAid, pk=request_id)

    if request.method == "POST":
        if "accept" in request.POST:
            percent_aid = int(request.POST["percent_aid"])
            aid_request.status = "accepted"
            aid_request.percent_aid = percent_aid
            aid_request.save()
            player = User.objects.get(username=aid_request.player_username).profile
            player.monthly_payment *= (100 - percent_aid) / 100
            player.save()
        elif "reject" in request.POST:
            aid_request.status = "rejected"
            aid_request.percent_aid = 0
            aid_request.save()
    return redirect('aid_requests')

def add_game(request):
    submitted = False
    if request.method == "POST":
        form = GameStat(request.POST)
        if form.is_valid():
            # Get the values of Team1 and Team2 from the form
            team1 = form.cleaned_data['Team1']
            team2 = form.cleaned_data['Team2']
            
            # Get the value of winner from the form
            Winner = form.cleaned_data['Winner']
            
            # Check that winner is either Team1 or Team2
            if Winner != team1 and Winner != team2:
                form.add_error('Winner', 'Winner must be either Team1 or Team2')
            else:
                form.save()
                return redirect('performance')    
    else:
        form = GameStat()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_game.html', {'form': form, 'submitted': submitted})


def update_game(request, games_id):
    games = Games.objects.get(id=games_id)
    form = GameStat(request.POST or None, request.FILES or None, instance=games)
    if form.is_valid():
        form.save()
        return redirect('performance')
    return render(request, 'update_game.html', {'games': games, 'form': form})

def delete_game(request, games_id):
    if request.method == "POST":
        if request.POST.get("confirm") == "yes":
            games = Games.objects.get(id=games_id)
            games.delete()
            return redirect('performance')
        else:
            return redirect("performance")    

    return render(request, 'confirm_delete_game.html')

from django.shortcuts import render
from .models import Stats
import random

def spin_the_wheel(request):
    # Get all players' stats
    player_stats = Stats.objects.all()

    # Find the player with the highest rating
    top_player = max(player_stats, key=lambda p: p.stat1)

    # Check if the user has already spun the wheel
    used_spin = request.session.get('used_spin', False)

    # Randomly decide whether to give a discount or not
    spin_result = None
    spin_outcomes = ["nothing", "nothing", "nothing", "10% off", "5% off", "15% off"]
    if random.random() < 0.5 and not used_spin:
        spin_result = random.choice(spin_outcomes)
        request.session['used_spin'] = True
    else:
        spin_result = "nothing"

    return render(request, 'spin_the_wheel.html', {'player': top_player, 'spin_result': spin_result, 'used_spin': used_spin})