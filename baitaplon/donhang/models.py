from django.db import models
from nguoidung.models import NguoiDung
from sanpham.models import SanPham

class DonHang(models.Model):
    TRANG_THAI_CHOICES = [
        ('cho_xu_ly', 'Chờ xử lý'),
        ('dang_giao', 'Đang giao hàng'),
        ('da_giao', 'Đã giao'),
        ('da_huy', 'Đã hủy'),
    ]

    ma_nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    ngay_dat = models.DateTimeField(auto_now_add=True)
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2)
    dia_chi_giao = models.CharField(max_length=255)
    phuong_thuc_thanh_toan = models.CharField(max_length=50)
    trang_thai_don_hang = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='cho_xu_ly')
    ghi_chu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.ma_nguoi_dung.ho_ten}"

class ChiTietDonHang(models.Model):
    ma_don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE, related_name="chi_tiet")
    ma_san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    so_luong = models.IntegerField()
    gia = models.DecimalField(max_digits=10, decimal_places=2)
    thanh_tien = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ma_san_pham.ten_san_pham} ({self.so_luong})"
