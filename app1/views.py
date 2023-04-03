from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def schedule(request):
    return render(request, 'schedule.html')

def communication(request):
    return render(request, 'communication.html')

def management(request):
    return render(request, 'management.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def performance(request):
    return render(request, 'performance.html')


from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the user's information to the database
            form.save()
            # Redirect the user to the login page
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})





		