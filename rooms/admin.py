from django.contrib import admin
from .models import Room, Message, Join

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Join)