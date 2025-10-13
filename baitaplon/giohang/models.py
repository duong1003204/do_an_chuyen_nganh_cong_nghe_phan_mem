from django.db import models

# Create your models here.
from django.db import models
from nguoidung.models import NguoiDung
from sanpham.models import SanPham

class GioHang(models.Model):
    ma_nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Giỏ hàng {self.ma_nguoi_dung.ho_ten}"


class ChiTietGioHang(models.Model):
    ma_gio_hang = models.ForeignKey(GioHang, on_delete=models.CASCADE)
    ma_san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    so_luong = models.IntegerField(default=1)
    ngay_them = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ma_san_pham.ten_san_pham} - {self.so_luong}"
