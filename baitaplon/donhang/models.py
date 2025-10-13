from django.db import models

# Create your models here.
from django.db import models
from nguoidung.models import NguoiDung
from sanpham.models import SanPham

class DonHang(models.Model):
    ma_nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    ngay_dat = models.DateTimeField(auto_now_add=True)
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2)
    dia_chi_giao = models.CharField(max_length=255)
    phuong_thuc_thanh_toan = models.CharField(max_length=50)
    trang_thai_don_hang = models.CharField(max_length=50, default='Đang xử lý')
    ghi_chu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Đơn hàng #{self.id}"


class ChiTietDonHang(models.Model):
    ma_don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE)
    ma_san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    so_luong = models.IntegerField()
    gia = models.DecimalField(max_digits=10, decimal_places=2)
    thanh_tien = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Chi tiết đơn {self.ma_don_hang.id}"
