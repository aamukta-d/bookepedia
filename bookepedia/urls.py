from django.urls import path
from bookepedia_project import views

app_name = 'bookepedia'

urlpatterns = [
    path('', views.homepage, name = 'homepage')
]
