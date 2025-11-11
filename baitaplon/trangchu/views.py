from django.shortcuts import render
from sanpham.models import DanhMuc, SanPham
from django.db.models import Count, Q


def index(request):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    danhmuc_slsp = DanhMuc.objects.filter(trang_thai=True).annotate(soluongsp=Count('sanpham'))

    sanpham_index = SanPham.objects.filter(trang_thai=True)
    sanpham_noibat = sanpham_index.order_by('-gia')[:8]
    
    return render(request, 'index.html', {'menudanhmuc': menudanhmuc, 'danhmuc_slsp': danhmuc_slsp, 'sanpham_index': sanpham_index, 'sanpham_noibat': sanpham_noibat})



def contact(request):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    return render(request, 'contact.html', {'menudanhmuc': menudanhmuc})

