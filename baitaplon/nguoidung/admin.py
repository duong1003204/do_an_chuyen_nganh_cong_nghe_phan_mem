from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NguoiDung

@admin.register(NguoiDung)
class NguoiDungAdmin(UserAdmin):
    list_display = ("username", "ho_ten", "email", "vai_tro", "is_staff", "trang_thai")
    list_filter = ("vai_tro", "is_staff", "trang_thai")

    fieldsets = (
        ("Thông tin tài khoản", {"fields": ("username", "password")}),
        ("Thông tin cá nhân", {"fields": ("ho_ten", "email", "so_dien_thoai", "dia_chi")}),
        ("Phân quyền", {"fields": ("vai_tro", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    def save_model(self, request, obj, form, change):
        # Phân quyền tự động theo vai trò
        if obj.vai_tro == 'admin':
            obj.is_staff = True
            obj.is_superuser = True
        elif obj.vai_tro == 'nhanvien':
            obj.is_staff = True
            obj.is_superuser = False
        else:  # khách hàng
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)
