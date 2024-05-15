from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class UserAuthenticationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password']




    #     class LoginForm(forms.Form):
    # username = forms.CharField(max_length=65)
    # password = forms.CharField(max_length=65, widget=forms.PasswordInput)