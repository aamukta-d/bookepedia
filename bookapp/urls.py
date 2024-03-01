from django.urls import path
from bookapp import views

app_name = 'bookepedia'

urlpatterns = [
    path('', views.homepage, name = 'homepage')
]
