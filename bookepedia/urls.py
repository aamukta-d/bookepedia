from django.urls import path
from bookepedia import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'bookepedia'

urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('add_a_book', views.add_a_book, name = 'add_a_book'),
    path('register/', views.register, name = 'register'),
    path('login/', views.user_login, name='user_login' ),
    path('profile/<username>', views.Profile.as_view(), name='profile'),
    path('search/', views.search, name='search'),
    path('logout/', views.user_logout, name='user_logout'),
    path('books/<slug:book_title_slug>/', views.show_book, name='show_book'),
    path('books/<slug:book_title_slug>/add_review/', views.add_review, name='add_review'),
    path('books/', views.all_books, name='all_books'),
]
