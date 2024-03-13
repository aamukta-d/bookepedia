from django.db import models
from django.contrib.auth.models import User


GENRE_CHOICES = [
    ('Fantasy', 'Fantasy'),
    ('Sci-Fi', 'Sci-Fi'),
]

class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


for genre_name, _ in GENRE_CHOICES:
    Genre.objects.get_or_create(name=genre_name)

class Book(models.Model):
    title = models.CharField(max_length=128, blank=True)
    author = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=128, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    top_genre = models.ManyToManyField(Genre)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
