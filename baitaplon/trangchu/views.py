from django.shortcuts import render
from sanpham.models import DanhMuc
from django.db.models import Count

def index(request):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    danhmuc_slsp = DanhMuc.objects.filter(trang_thai=True).annotate(soluongsp=Count('sanpham'))
    return render(request, 'index.html', {'menudanhmuc': menudanhmuc, 'danhmuc_slsp': danhmuc_slsp})
