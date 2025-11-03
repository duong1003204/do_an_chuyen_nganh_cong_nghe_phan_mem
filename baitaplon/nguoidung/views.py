from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages



# Create your views here.
def login(request):
    

    
    
    return render(request, 'login.html')