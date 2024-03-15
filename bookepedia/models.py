from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=128, blank=True, unique=True)
    author = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=128, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE) 
    cover = models.ImageField(upload_to='book_covers', blank = True)
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) 
        super(Book, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    top_genre = models.ManyToManyField(Genre)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
