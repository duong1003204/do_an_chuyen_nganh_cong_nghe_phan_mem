# urls.py (trong app, ví dụ: accounts/urls.py)

from django.urls import path
from . import views


urlpatterns = [
    path('dang-nhap/', views.customer_login, name='dang-nhap'),
]