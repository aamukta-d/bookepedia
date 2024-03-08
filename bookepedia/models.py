from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length = 128, blank = True)
    author = models.CharField(max_length = 128, blank = True)
    description = models.CharField(max_length = 128, blank = True)

    def __str__(self): 
        return self.title
