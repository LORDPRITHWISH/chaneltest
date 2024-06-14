from django.db import models
from django.contrib.auth.models import User
import random
import string


class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def generate_slug(self, length=10):
        while True:
            ran = ''.join(random.choice(string.ascii_letters) for _ in range(length))
            if not Room.objects.filter(slug=ran).exists():
                return ran

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['created']

class Join(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']