from django.db import models

class Book(models.Model):
    title = models.CharField(max_length = 128, blank = True)
    author = models.CharField(max_length = 128, blank = True)
    description = models.CharField(max_length = 128, blank = True)
    GENRE_CHOICES = [
        ('Fantasy', 'Fantasy'),
        ('Sci-Fi', 'Sci-Fi'),
    ]
    genre = models.CharField(max_length=128, choices=GENRE_CHOICES, help_text="Please select a genre.")
    def __str__(self): 
        return self.title