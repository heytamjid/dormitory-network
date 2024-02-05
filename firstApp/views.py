from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from datetime import datetime



def landing(request):
    return render(request, "firstApp/landing.html")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')  # Replace 'home' with the URL you want to redirect to after signup
    else:
        form = SignUpForm()
    return render(request, 'firstApp/signup.html', {'form': form})


def loginFunc(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Replace 'home' with the URL you want to redirect to after login
    else:
        form = LoginForm()
    return render(request, 'firstApp/login.html', {'form': form})

@login_required
def logoutFunc(request):
    logout(request)
    return redirect('landing') 

@login_required
def dashboard (request):
    username = request.user.username
    return render (request, 'firstApp/dashboard.html', {
        'username' : username,
    })
    
    

    
@login_required
def start_timer(request):
    start_time = timezone.now()
    request.session['start_time'] = start_time.timestamp() 
    return HttpResponse("<button type='submit' id='endTimerButton' hx-get='/endTimerClicked/' hx-target='#endTimerButton' hx-swap='outerHTML'> Stop Tracking </button>")

@login_required
def stop_timer(request):
    end_time = timezone.now().timestamp()
    start_time = request.session['start_time']
    duration = (end_time - start_time)

    #TrackedTimeDB te UTC+0 onujayi save ache time. User er timezoneinfo onujayi +- kore user ke show korte hobe
    TrackedTimeDB.objects.create(user=request.user, startTime=datetime.fromtimestamp(start_time), endTime=datetime.fromtimestamp(end_time), duration=timezone.timedelta(seconds=duration))
    del request.session['start_time']

    return HttpResponse("<button type='submit' id='startTimerButton' hx-get='/startTimerClicked/' hx-target='#startTimerButton' hx-swap='outerHTML'> Start Tracking </button>")

#ei porjonto. model e save hocche stop korle.
#ekhon stop korle dashboard e agergula + save howa entry gulo show korar bebostha korte hobe. 