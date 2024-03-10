from django.shortcuts import render
from django.http import HttpResponse
from bookepedia.forms import BookForm
from django.shortcuts import redirect

# Create your views here.

def homepage(request):
    return render(request, 'bookepedia/homepage.html')

def add_a_book(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)

    if form.is_valid():
    # Save the new category to the database. 
        form.save(commit=True)
    # Now that the category is saved, we could confirm this. # For now, just redirect the user back to the index view. 
        return redirect('/bookepedia/')
    
    else:
        print(form.errors)

    return render(request, 'bookepedia/add_a_book.html', {'form': form})

def register(request):
    return render(request, 'bookepedia/Registration.html')

