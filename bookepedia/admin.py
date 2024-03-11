from django.contrib import admin
from bookepedia.models import Book
from bookepedia.models import UserProfile

# Register your models here.

admin.site.register(Book)
admin.site.register(UserProfile)