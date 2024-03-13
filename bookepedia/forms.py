from django import forms
from .models import Book
from django.contrib.auth.models import User
from bookepedia.models import UserProfile
from .models import GENRE_CHOICES

class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the book.")
    author = forms.CharField(max_length=128, help_text="Please enter the author's name.")
    description = forms.CharField(max_length=128, help_text="Please provide a short description.")

    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'genre')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta: 
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm): 

    top_genre = forms.MultipleChoiceField(
        choices = GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = UserProfile
        fields = ('picture', 'top_genre',)
