from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from bookepedia.forms import BookForm
from django.shortcuts import redirect, get_object_or_404
from bookepedia.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from .models import Genre
from .models import Book
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from bookepedia.models import UserProfile
from django.contrib.auth.decorators import login_required
from bookepedia.models import UserBookInteraction , get_books_by_user_genre
from bookepedia.models import Comment
from bookepedia.forms import CommentForm
from bookepedia.bing_search import run_query

# Create your views here.

def homepage(request):
    context_dict = {}
    context_dict['logged_in'] = request.user.is_authenticated
    if request.user.is_authenticated:
        user = request.user
        recommended_books = get_books_by_user_genre(user, limit=3)
        context_dict['recommended_books'] = recommended_books
    
    return render(request, 'bookepedia/homepage.html', context = context_dict)

def add_a_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            
            cover = request.FILES.get('cover')
            form.instance.cover = cover  

            form.save()
            return redirect('/bookepedia/')
    else:
        form = BookForm()
    
    return render(request, 'bookepedia/add_a_book.html', {'form': form})

def show_book(request, book_title_slug):
    context_dict = {}
    logged_in = request.user.is_authenticated
    if request.user.is_authenticated:
         
        user_profile = UserProfile.objects.get(user=request.user)
        books = user_profile.top_picks.all()
        context_dict['books'] = books
        context_dict['user_profile'] = user_profile

    book = Book.objects.get(slug=book_title_slug)
    comments = book.comments.all()
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    
    context_dict['book'] = book
    context_dict['comments'] = comments
    context_dict['new_comment'] = new_comment
    context_dict['comment_form'] = comment_form
    context_dict['logged_in'] = logged_in
    
    return render(request, 'bookepedia/book.html', context_dict)

def add_review(request, book_title_slug):
    book = Book.objects.get(slug=book_title_slug)
    
    if request.method == 'POST':
        review_form = CommentForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.user = request.user
            new_review.save()
            return redirect('bookepedia:show_book', book_title_slug=book_title_slug)
    else:
        review_form = CommentForm()
    
    return render(request, 'bookepedia/add_review.html', {'book': book, 'review_form': review_form})

def add_to_top_picks(request, book_slug):
    book = Book.objects.get(slug=book_slug)
    user_profile = UserProfile.objects.get(user=request.user)
    
    if book not in user_profile.top_picks.all():
        user_profile.top_picks.add(book)

  
    return redirect('bookepedia:show_book', book.slug)

def all_books(request):
    books = Book.objects.all()
    logged_in = request.user.is_authenticated
    return render(request, 'bookepedia/all_books.html', {'books': books, 'logged_in':logged_in})

def search(request): 
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip() 
        if query:
            result_list = run_query(query)
    return render(request, 'bookepedia/search.html', {'result_list': result_list})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('bookepedia:homepage'))

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
                
                selected_genres = Genre.objects.filter(name__in=selected_genre_names)
                

                profile.top_genre.set(selected_genres)

            profile.save()

            registered = True


        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'bookepedia/Registration.html', 
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
            messages.error(request, "Invalid login details provided. Register instead?") 

    return render(request, 'bookepedia/Login.html')

class Profile(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        form = UserProfileForm(instance=user_profile)
        return user, user_profile, form

    def get(self, request, username):
        user, user_profile, form = self.get_user_details(username)
        if user is None:
            return redirect(reverse('bookepedia:register'))
        
        context_dict = {
            'user_profile': user_profile,
            'selected_user': user,
            'form': form,          
        }

        return render(request, 'bookepedia/user_profile.html', context_dict)

