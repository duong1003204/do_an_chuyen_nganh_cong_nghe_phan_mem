
from django.urls import include, path

from nguoidung import views
from .views import login,dangki

urlpatterns = [
   path('login/', login, name='login'),
   path('dangki/', dangki, name='dangki' ),
]