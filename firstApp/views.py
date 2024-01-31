from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required




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