# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NguoiDung
from .forms import NguoiDungCreationForm, NguoiDungChangeForm

@admin.register(NguoiDung)
class NguoiDungAdmin(UserAdmin):
    add_form = NguoiDungCreationForm
    form = NguoiDungChangeForm
    model = NguoiDung

    list_display = ['username', 'ho_ten', 'email', 'vai_tro', 'is_staff', 'trang_thai']

    # GHI ĐÈ HOÀN TOÀN fieldsets - KHÔNG DÙNG +
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Thông tin cá nhân', {
            'fields': ('ho_ten', 'email', 'so_dien_thoai', 'dia_chi')
        }),
        ('Quyền hạn', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Thông tin bổ sung', {
            'fields': ('vai_tro', 'trang_thai'),
            'classes': ('collapse',)
        }),
    )

    # GHI ĐÈ HOÀN TOÀN add_fieldsets - KHÔNG DÙNG +
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Thông tin cá nhân', {
            'fields': ('ho_ten', 'email', 'so_dien_thoai', 'dia_chi', 'vai_tro', 'trang_thai'),
        }),
    )