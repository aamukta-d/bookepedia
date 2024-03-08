from django import forms 
from bookepedia.models import Book

class BookForm(forms.ModelForm):
    title = forms.CharField(max_length = 128, help_text = "Please enter the title of the book.")
    author = forms.CharField(max_length = 128, help_text = "Please enter the author's name.")
    description = forms.CharField(max_length = 128, help_text = "Please provide a short description.")

    class Meta:
        model = Book
        fields = ('title','author','description','genre')