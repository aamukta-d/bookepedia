from django.urls import path
from bookepedia import views

app_name = 'bookepedia'

urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('add_a_book', views.add_a_book, name = 'add_a_book'),
    path('register', views.register, name = 'register')
]
