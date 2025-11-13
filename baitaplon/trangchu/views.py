from django.shortcuts import render
from sanpham.models import DanhMuc, SanPham
from django.db.models import Count, Q
from django.core.paginator import Paginator  # <-- IMPORT DÒNG NÀY

def index(request):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    danhmuc_slsp = DanhMuc.objects.filter(trang_thai=True).annotate(soluongsp=Count('sanpham'))

    # SẢN PHẨM NỔI BẬT (Giữ nguyên, không phân trang)
    sanpham_noibat = SanPham.objects.filter(trang_thai=True).order_by('-gia')[:8]
    
    # --- PHẦN PHÂN TRANG CHO SẢN PHẨM GẦN ĐÂY ---
    # 1. Lấy TẤT CẢ sản phẩm (thay vì giới hạn 8)
    sanpham_list = SanPham.objects.filter(trang_thai=True).order_by('-id')

    # 2. Tạo Paginator (ví dụ: 8 sản phẩm mỗi trang)
    paginator = Paginator(sanpham_list, 8)
    
    # 3. Lấy số trang từ URL (ví dụ: ?page=1)
    page_number = request.GET.get('page')
    
    # 4. Lấy các sản phẩm cho trang đó
    # Biến này (sanpham_page) sẽ được gửi sang template
    sanpham_page = paginator.get_page(page_number)
    # --- Hết phần phân trang ---
    
    
    context = {
        'menudanhmuc': menudanhmuc,
        'danhmuc_slsp': danhmuc_slsp,
        'sanpham_noibat': sanpham_noibat, # 8 sản phẩm nổi bật
        'sanpham_page': sanpham_page      # <-- THAY sanpham_index BẰNG sanpham_page
    }
    return render(request, 'index.html', context)


def contact(request):
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)
    return render(request, 'contact.html', {'menudanhmuc': menudanhmuc})