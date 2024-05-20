from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    propic=models.ImageField(default='default.jpg',upload_to='profile_pics')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\' Profile'

    class Meta:
        ordering = ['created']


