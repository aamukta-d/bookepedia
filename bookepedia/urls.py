from django.urls import path
from bookepedia import views

app_name = 'bookepedia'

urlpatterns = [
    path('', views.homepage, name = 'homepage')
]
