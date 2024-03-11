from django.db import models
from django.contrib.auth.models import User

GENRE_CHOICES = [
        ('Fantasy', 'Fantasy'),
        ('Sci-Fi', 'Sci-Fi'),
    ]

class Book(models.Model):
    title = models.CharField(max_length = 128, blank = True)
    author = models.CharField(max_length = 128, blank = True)
    description = models.CharField(max_length = 128, blank = True)

    genre = models.CharField(max_length=128, choices=GENRE_CHOICES, help_text="Please select a genre.")
    def __str__(self): 
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    top_genre = models.CharField(max_length = 128, choices=GENRE_CHOICES, default='Fantasy')

    def __str__(self):
        return self.user.username 