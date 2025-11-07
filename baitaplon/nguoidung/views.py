# views.py (trong app của bạn, ví dụ: accounts/views.py)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse

# views.py
def customer_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.trang_thai and user.vai_tro == 'khachhang':
            login(request, user)
            messages.success(request, f"Chào mừng {user.ho_ten}!")
            return redirect('index')  # ← QUAN TRỌNG: redirect, không render lại form
        else:
            messages.error(request, "Đăng nhập thất bại.")

    return render(request, 'login.html')