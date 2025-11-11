# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ajax/search/', views.search_suggestions, name='search_suggestions'),
]