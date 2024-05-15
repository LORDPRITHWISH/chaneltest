from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from . import forms

def home(request):
    return render(request, 'calci/home.html')

def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            login(request, user)
            return redirect('calci-home')
    else:
        print("Form is not at all valid")
        form = forms.UserRegisterForm()
    return render(request, 'calci/register.html', {'form':form})

def room(request):
    return render(request, 'calci/room.html')

def logoutcall(request):
    logout(request)
    return redirect('calci-home')

    # return render(request, 'calci/logout.html')