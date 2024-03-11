from django.shortcuts import render
from django.http import HttpResponse
from bookepedia.forms import BookForm
from django.shortcuts import redirect
from bookepedia.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User

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
    registered = False
    user_form = UserForm()
    profile_form = UserProfileForm()

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
            
            user = user_form.save(commit=False)
            user.set_password(user.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'top_genre' in request.POST:
                profile.top_genre = request.POST['top_genre']
                
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    return render(request, 'bookepedia/registration.html', 
    {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })

