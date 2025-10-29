from django.http import JsonResponse
from django.shortcuts import render
from .models import DanhMuc, SanPham, BienTheSanPham

def chitietsanpham(request, id):
    ctsp = SanPham.objects.get(id=id)
    sizes = list(ctsp.bienthesanpham_set.values_list('kich_thuoc', flat=True).distinct())
    colors = list(ctsp.bienthesanpham_set.values_list('mau_sac', flat=True).distinct())
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)

    return render(request, 'detail.html', {'ctsp': ctsp, 'sizes': sizes, 'colors': colors, 'menudanhmuc': menudanhmuc})

def colors_for_size(request):
    size = request.GET.get('size')
    sp_id = request.GET.get('sp_id')
    bien_the = BienTheSanPham.objects.filter(ma_san_pham_id=sp_id, kich_thuoc=size)
    colors = list(bien_the.values_list('mau_sac', flat=True).distinct())
    return JsonResponse({'colors': colors})


def image_for_variant(request):
    size = request.GET.get('size')
    color = request.GET.get('color')
    sp_id = request.GET.get('sp_id')
    bt = BienTheSanPham.objects.filter(ma_san_pham_id=sp_id, kich_thuoc=size, mau_sac=color).first()
    if bt and bt.hinh_anh:
        img_url = bt.hinh_anh.url
    else:
        img_url = ''
    return JsonResponse({'img_url': img_url})

def shop(request):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    sanpham = SanPham.objects.all()
    return render(request, 'shop.html', {'menudanhmuc': menudanhmuc, 'sanpham': sanpham})

def shop_danhmuc(request, id):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    danhmuc = DanhMuc.objects.get(id=id)
    sanpham = SanPham.objects.filter(ma_danh_muc_id=id)

    return render(request, 'shop.html', {'menudanhmuc': menudanhmuc, 'danhmuc': danhmuc, 'sanpham': sanpham})