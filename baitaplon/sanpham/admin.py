from django.contrib import admin

# Register your models here.

from .models import DanhMuc, SanPham,BienTheSanPham

admin.site.register(DanhMuc)
admin.site.register(SanPham)
admin.site.register(BienTheSanPham)