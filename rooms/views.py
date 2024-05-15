from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Room

@login_required
def rooms(request):
    roms = Room.objects.all()
    return render(request, 'rooms/rooms.html', {'rooms':roms,'title':'Rooms'})

def room(request,slug):
    rom = Room.objects.get(slug=slug)
    return render(request, 'rooms/room.html', {'room':rom,'title':rom.name})