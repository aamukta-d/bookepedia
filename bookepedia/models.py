from django.db import models

# Create your models here.

class Book(models.Model):
    GENRE_CHOICES = [
        ('Fantasy', 'Fantasy'),
        ('Sci_Fi', 'Sci-Fi')
    ]
    title = models.CharField(max_length = 128, blank = True)
    author = models.CharField(max_length = 128, blank = True)
    description = models.CharField(max_length = 128, blank = True)
    genre = models.CharField(max_length=128, choices=GENRE_CHOICES, help_text = "Please select a genre.")

    def __str__(self): 
        return self.title