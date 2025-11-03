from django.shortcuts import render
from sanpham.models import SanPham
from django.http import HttpRequest



# Create your views here.
def them_vao_gio_hang():
    pass
def xem_gio_hang(request: HttpRequest):
    san_pham = SanPham.objects.all()
    return render(request, 'giohang.html', {'san_pham': san_pham})