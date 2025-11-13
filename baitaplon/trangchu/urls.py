
from django.urls import include, path

from giohang import views
from .views import index, contact

urlpatterns = [
    path('',index, name = 'index'),
    
    path('contact/', contact, name='contact'),
]
