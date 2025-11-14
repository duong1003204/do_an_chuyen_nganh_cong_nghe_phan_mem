from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NguoiDung
from .forms import NguoiDungCreationForm, NguoiDungChangeForm # <-- IMPORT FORM MỚI

class NguoiDungAdmin(UserAdmin):
    add_form = NguoiDungCreationForm  # Form khi *thêm mới* user trong admin
    form = NguoiDungChangeForm      # Form khi *chỉnh sửa* user trong admin
    model = NguoiDung
    
    list_display = ['username', 'ho_ten', 'email', 'vai_tro', 'is_staff', 'trang_thai']
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('ho_ten', 'so_dien_thoai', 'dia_chi', 'vai_tro', 'trang_thai')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('ho_ten', 'email', 'so_dien_thoai', 'dia_chi', 'vai_tro', 'trang_thai')}),
    )

admin.site.register(NguoiDung, NguoiDungAdmin)