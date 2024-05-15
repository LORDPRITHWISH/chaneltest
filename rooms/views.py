from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Room

@login_required
def rooms(request):
    rom = Room.objects.all()
    return render(request, 'rooms/rooms.html', {'rooms':rom})

def room(request,slug):
    return render(request, 'rooms/room.html')