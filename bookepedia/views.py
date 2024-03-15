from django.shortcuts import render
from django.http import HttpResponse
from bookepedia.forms import BookForm
from django.shortcuts import redirect
from bookepedia.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from .models import Genre
from .models import Book
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

def homepage(request):
    context_dict = {}
    context_dict['logged_in'] = request.user.is_authenticated
    
    return render(request, 'bookepedia/homepage.html', context = context_dict)

def add_a_book(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            if 'cover' in request.FILES:
                form.cover = request.FILES['cover'] 
    
            form.save(commit=True)
            return redirect('/bookepedia/')
           
        else:
            print(form.errors)

    return render(request, 'bookepedia/add_a_book.html', {'form': form})

def show_book(request, book_title_slug):
    book = Book.objects.get(slug=book_title_slug)
    return render(request, 'bookepedia/book.html', {'book':book})

def register(request):

    genres = Genre.objects.all()

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['username']

            if User.objects.filter(username=username).exists():
                return render(request, 'bookepedia/registration.html', {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'error_message': 'Username is already taken'
                })
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture'] 

            profile.save()

            if 'top_genre' in request.POST:
                selected_genre_names = request.POST.getlist('top_genre')  
                
                # Retrieve Genre objects based on the selected genre names
                selected_genres = Genre.objects.filter(name__in=selected_genre_names)
                
                # Set the selected genres for the UserProfile instance
                profile.top_genre.set(selected_genres)

            profile.save()

            registered = True


        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'bookepedia/registration.html', 
    {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        'genres': genres
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('bookepedia:homepage'))  
            else:
                messages.error(request, "Your account is disabled.")
        else:
            messages.error(request, "Invalid login details provided.")

        return redirect(reverse('bookepedia:register'))
        

    return render(request, 'bookepedia/Login.html')
