from attr import mutable
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    propic=models.ImageField(default='default.jpg',upload_to='profile_pic')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    bio = models.TextField(default='not set')
    name = models.CharField(max_length=50,default=User.username)


    def __str__(self):
        return f'{self.user.username}\' Profile'



