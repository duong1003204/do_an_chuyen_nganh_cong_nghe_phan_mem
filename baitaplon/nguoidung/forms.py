# users/forms.py  (hoặc tên app của bạn)
from django import forms
from django.contrib.auth import authenticate
from .models import NguoiDung

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tài khoản',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu',
            'autocomplete': 'current-password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Tài khoản hoặc mật khẩu không đúng.")
            if not user.trang_thai:
                raise forms.ValidationError("Tài khoản của bạn đã bị khóa.")
            cleaned_data['user'] = user
        return cleaned_data