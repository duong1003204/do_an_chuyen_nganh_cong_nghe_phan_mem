
from django.urls import include, path

from nguoidung import views
from .views import login

urlpatterns = [
   path('login/', login, name='login'),
]