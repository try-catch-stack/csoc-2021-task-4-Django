from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


def loginView(request):
    if request.method == 'POST':
        loginUsername = request.POST['username']
        loginPassword = request.POST['password']
        user = authenticate(username=loginUsername,
                            password=loginPassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('book-list')
        else:
            messages.error(request, "Invalid credentials.")
            return render(request, 'authentication/login.html')
    return render(request, 'authentication/login.html')


def logoutView(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


def registerView(request):
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if(len(username) < 5):
            messages.error(
                request, 'Username must be at least 5 characters long.')

        elif User.objects.filter(email=email).exists():
            messages.error(
                request, 'User with this email already exists')
            return render(request, 'authentication/register.html')
        else:
            try:
                newUser = User.objects.create_user(
                    username=username, email=email, password=password)
                login(request, newUser)
                messages.success(request, 'User registered successfully.')
                return redirect('book-list')
            except:
                messages.error(
                    request, 'User with this username already exists')
                return render(request, 'authentication/register.html')

    return render(request, 'authentication/register.html')
