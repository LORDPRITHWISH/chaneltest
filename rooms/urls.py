from django.urls import path
from . import views

urlpatterns = [
    path('',views.rooms, name='calci-room'),
    path('<slug:slug>/',views.room, name='room'),

]
