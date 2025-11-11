from django.http import JsonResponse
from django.shortcuts import render
from .models import DanhMuc, SanPham, BienTheSanPham
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from .models import SanPham
from django.core.paginator import Paginator

# --- Các view chitietsanpham, colors_for_size, image_for_variant giữ nguyên ---
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

# --- CẬP NHẬT VIEW SHOP ---
def shop(request):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    sanpham_list = SanPham.objects.filter(trang_thai=True).order_by('id')

    # BỔ SUNG: Lấy tất cả màu và size để hiển thị bộ lọc
    # Lấy các giá trị không rỗng và sắp xếp
    all_colors = BienTheSanPham.objects.exclude(mau_sac__isnull=True).exclude(mau_sac__exact='').values_list('mau_sac', flat=True).distinct().order_by('mau_sac')
    all_sizes = BienTheSanPham.objects.exclude(kich_thuoc__isnull=True).exclude(kich_thuoc__exact='').values_list('kich_thuoc', flat=True).distinct().order_by('kich_thuoc')

    query = request.GET.get('timkiem')
    if query:
        sanpham_list = sanpham_list.filter(
            Q(ten_san_pham__icontains=query) | Q(mo_ta__icontains=query)
        )

    # --- LOGIC LỌC NÂNG CAO (Giữ nguyên từ trước) ---
    selected_prices = request.GET.getlist('price')
    selected_colors = request.GET.getlist('color')
    selected_sizes = request.GET.getlist('size')

    if selected_prices:
        price_query = Q()
        if "0-100" in selected_prices: price_query.add(Q(gia__gte=0, gia__lte=100), Q.OR)
        if "100-200" in selected_prices: price_query.add(Q(gia__gte=100, gia__lte=200), Q.OR)
        if "200-300" in selected_prices: price_query.add(Q(gia__gte=200, gia__lte=300), Q.OR)
        if "300-400" in selected_prices: price_query.add(Q(gia__gte=300, gia__lte=400), Q.OR)
        if "400-500" in selected_prices: price_query.add(Q(gia__gte=400, gia__lte=500), Q.OR)
        
        if price_query:
            sanpham_list = sanpham_list.filter(price_query)

    if selected_colors:
        sanpham_list = sanpham_list.filter(bienthesanpham__mau_sac__in=selected_colors).distinct()

    if selected_sizes:
        sanpham_list = sanpham_list.filter(bienthesanpham__kich_thuoc__in=selected_sizes).distinct()
    # --- KẾT THÚC LOGIC LỌC ---

    paginator = Paginator(sanpham_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop.html', {
        'menudanhmuc': menudanhmuc,
        'sanpham': page_obj,
        'query': query,
        
        'all_colors': all_colors, # <-- Gửi data động
        'all_sizes': all_sizes,   # <-- Gửi data động
        
        'selected_prices': selected_prices,
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
    })

# --- CẬP NHẬT VIEW SHOP_DANHMUC ---
def shop_danhmuc(request, id):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    danhmuc = DanhMuc.objects.get(id=id)
    sanpham_list = SanPham.objects.filter(ma_danh_muc_id=id).order_by('id')

    # BỔ SUNG: Lấy tất cả màu và size để hiển thị bộ lọc
    all_colors = BienTheSanPham.objects.exclude(mau_sac__isnull=True).exclude(mau_sac__exact='').values_list('mau_sac', flat=True).distinct().order_by('mau_sac')
    all_sizes = BienTheSanPham.objects.exclude(kich_thuoc__isnull=True).exclude(kich_thuoc__exact='').values_list('kich_thuoc', flat=True).distinct().order_by('kich_thuoc')

    # --- LOGIC LỌC NÂNG CAO (Giữ nguyên từ trước) ---
    selected_prices = request.GET.getlist('price')
    selected_colors = request.GET.getlist('color')
    selected_sizes = request.GET.getlist('size')

    if selected_prices:
        price_query = Q()
        if "0-100" in selected_prices: price_query.add(Q(gia__gte=0, gia__lte=100), Q.OR)
        if "100-200" in selected_prices: price_query.add(Q(gia__gte=100, gia__lte=200), Q.OR)
        if "200-300" in selected_prices: price_query.add(Q(gia__gte=200, gia__lte=300), Q.OR)
        if "300-400" in selected_prices: price_query.add(Q(gia__gte=300, gia__lte=400), Q.OR)
        if "400-500" in selected_prices: price_query.add(Q(gia__gte=400, gia__lte=500), Q.OR)
        
        if price_query:
            sanpham_list = sanpham_list.filter(price_query)

    if selected_colors:
        sanpham_list = sanpham_list.filter(bienthesanpham__mau_sac__in=selected_colors).distinct()

    if selected_sizes:
        sanpham_list = sanpham_list.filter(bienthesanpham__kich_thuoc__in=selected_sizes).distinct()
    # --- KẾT THÚC LOGIC LỌC ---

    paginator = Paginator(sanpham_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop.html', {
        'menudanhmuc': menudanhmuc, 
        'danhmuc': danhmuc, 
        'sanpham': page_obj,
        
        'all_colors': all_colors, # <-- Gửi data động
        'all_sizes': all_sizes,   # <-- Gửi data động

        'selected_prices': selected_prices,
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
    })