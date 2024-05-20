from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User


def home(request):
    return render(request, 'calci/home.html', {'title':'Home'})


def about(request):
    return render(request, 'calci/about.html', {'title':'About Us'})


def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            login(request, user)
            return redirect('calci-home')
        print("Form is not at all valid")
    else:
        print("ist entry time")
        form = forms.UserRegisterForm()
    return render(request, 'calci/register.html', {'form':form, 'title':'Register'})


def profile(request,username):
    user=User.objects.filter(username=username)
    # profile=
    return render(request, 'calci/profile.html', {'user':user, 'title':f'{username}\'s Profile'})


def logoutcall(request):
    logout(request)
    return redirect('calci-home')

    # return render(request, 'calci/logout.html')