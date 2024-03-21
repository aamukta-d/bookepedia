from django import forms
from .models import Book
from django.contrib.auth.models import User
from bookepedia.models import UserProfile
from bookepedia.models import Genre
from bookepedia.models import Comment

class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the book.")
    author = forms.CharField(max_length=128, help_text="Please enter the author's name.")
    description = forms.CharField(max_length=600, help_text="Please provide a short description.")

    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'cover', 'genre')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta: 
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm): 
    top_genre = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple
    )
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['top_genre'].choices = [(genre.name, genre.name) for genre in Genre.objects.all()]

    class Meta:
        model = UserProfile
        fields = ('picture', 'top_genre',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
    