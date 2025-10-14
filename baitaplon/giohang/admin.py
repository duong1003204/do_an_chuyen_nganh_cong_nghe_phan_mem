from django.contrib import admin

# Register your models here.
from .models import GioHang, ChiTietGioHang

admin.site.register(GioHang)
admin.site.register(ChiTietGioHang)