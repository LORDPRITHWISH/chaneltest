from re import M
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Room, Message, Join

@login_required
def rooms(request):
    roms = Room.objects.all()
    return render(request, 'rooms/rooms.html', {'rooms':roms,'title':'Rooms'})

@login_required
def room(request,slug):
    rom = Room.objects.get(slug=slug)
    mess = Message.objects.filter(room=rom)
    mem = Join.objects.filter(room=rom)
    onli = mem.count()
    return render(request, 'rooms/room.html', {'room':rom,'title':rom.name,'messages':mess,'members':mem,'online':onli})