from django.contrib import admin
from .models import DonHang, ChiTietDonHang

class ChiTietDonHangInline(admin.TabularInline):
    model = ChiTietDonHang
    extra = 0
    readonly_fields = ['ma_san_pham', 'so_luong', 'gia', 'thanh_tien']

@admin.register(DonHang)
class DonHangAdmin(admin.ModelAdmin):
    list_display = ['id', 'ma_nguoi_dung', 'ngay_dat', 'tong_tien', 'trang_thai_don_hang']
    list_filter = ['trang_thai_don_hang', 'ngay_dat']
    search_fields = ['ma_nguoi_dung__ho_ten', 'id']
    inlines = [ChiTietDonHangInline]
    readonly_fields = ['ngay_dat', 'tong_tien']

    actions = ['xac_nhan_don', 'danh_dau_da_giao', 'huy_don']

    @admin.action(description="✅ Xác nhận đơn hàng")
    def xac_nhan_don(self, request, queryset):
        queryset.update(trang_thai_don_hang='dang_giao')

    @admin.action(description="📦 Đánh dấu đã giao")
    def danh_dau_da_giao(self, request, queryset):
        queryset.update(trang_thai_don_hang='da_giao')

    @admin.action(description="❌ Hủy đơn hàng")
    def huy_don(self, request, queryset):
        queryset.update(trang_thai_don_hang='da_huy')
