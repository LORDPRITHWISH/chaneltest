from os import name
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile


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
            return redirect('home')
        print("Form is not at all valid", form.errors)
        return render(request, 'calci/register.html', {'form':form, 'title':'Register', 'errors':form.errors})

    else:
        print("ist entry time")
        form = forms.UserRegisterForm()
    return render(request, 'calci/register.html', {'form':form, 'title':'Register'})


def profile(request,username):
    user=User.objects.filter(username=username).first()
    return render(request, 'calci/profile.html', {'user':user, 'title':f'{username}\'s Profile'})


def editprofile(request,username):
    user=User.objects.filter(username=username).first()
    # print(user)
    return render(request, 'calci/setprofile.html', {'user':user, 'title':f'{username}\'s Profile'})
    

def setprofile(request,username):
    if request.method == 'POST':
        name = request['POST'].username
        print(name)
        return render(request, 'calci/setprofile.html', {'form':form, 'title':'Set Profile', 'errors':form.errors})

    else:
        print("ist entry time")
        form = forms.ProfileForm()
    pro = Profile.objects.filter(user__username=username).first()
    return render(request, 'calci/setprofile.html', {'form':form, 'title':'Set Profile'})

def logoutcall(request):
    logout(request)
    return redirect('home')

    # return render(request, 'calci/logout.html')

def upload_media(request):
    return render(request, 'calci/upload_media.html')