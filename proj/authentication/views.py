import logging

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=email):
            messages.error(request, "User with this e-mail address already exists!")
            return redirect('home')
        if len(email) > 30:
            messages.error(request, "E-mail can be up to 20 characters long")
            return redirect('home')
        if password != password2:
            messages.error(request, "Password are not the same!")
            return redirect('home')
        if not firstname.isalpha:
            messages.error(request, "First name may only consist of letters of the alphabet ")
            return redirect('home')
        if not lastname.isalpha:
            messages.error(request, "Last name may only consist of letters of the alphabet ")
            return redirect('home')

        user = User.objects.create_user(username=email, password=password)
        user.first_name = firstname
        user.last_name = lastname

        user.save()

        messages.success(request, "Account successfully created!")

        return redirect('signin')


    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return render(request, "authentication/index.html")
        else:
            messages.error(request, "Wrong credentials!")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out!")
    return redirect('home')

