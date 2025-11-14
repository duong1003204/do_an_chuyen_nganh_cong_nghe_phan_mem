from django.db import models

# Create your models here.
class DanhMuc(models.Model):
    ten_danh_muc = models.CharField(max_length=100)
    mo_ta = models.TextField(blank=True, null=True)
    trang_thai = models.BooleanField(default=True)
    
    def __str__(self):
        return self.ten_danh_muc
    
class SanPham(models.Model):
    ma_danh_muc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE)
    ten_san_pham = models.CharField(max_length=200)
    mo_ta = models.TextField(blank=True, null=True)
    gia = models.DecimalField(max_digits=10, decimal_places=2)
    giakm = models.DecimalField(max_digits=10, decimal_places=2)
    anh_dai_dien = models.ImageField(upload_to='sanpham/', blank=True, null=True)
    trang_thai = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.ten_san_pham} - {self.ma_danh_muc.ten_danh_muc} - {self.gia} - {self.trang_thai} - {self.anh_dai_dien}"
    
class BienTheSanPham(models.Model):
    ma_san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    kich_thuoc = models.CharField(max_length=50, blank=True, null=True)
    mau_sac = models.CharField(max_length=50, blank=True, null=True)
    so_luong = models.PositiveIntegerField(default=0)
    hinh_anh = models.ImageField(upload_to='sanpham/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.ma_san_pham.ten_san_pham} - {self.kich_thuoc} - {self.mau_sac} - {self.so_luong} - {self.hinh_anh}"
    

