from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='calci-home'),
    path('register/',views.register, name='register'),
    path('logout/',views.logoutcall, name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='calci/login.html',), name='login'),
]
