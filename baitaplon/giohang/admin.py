from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GioHang, ChiTietGioHang

class ChiTietGioHangInline(admin.TabularInline):
    model = ChiTietGioHang
    extra = 0  # không thêm dòng trống
    readonly_fields = ('ma_san_pham', 'so_luong', 'ngay_them')

@admin.register(GioHang)
class GioHangAdmin(admin.ModelAdmin):
    list_display = ('ma_nguoi_dung', 'ngay_tao', 'ngay_cap_nhat')
    search_fields = ('ma_nguoi_dung__ho_ten',)
    inlines = [ChiTietGioHangInline]
