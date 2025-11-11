from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from sanpham.models import DanhMuc, SanPham
from .models import GioHang, ChiTietGioHang
from django.contrib import messages

@require_POST
def them_vao_gio_hang(request):
    san_pham_id = request.POST.get('san_pham_id')
    
    size = request.POST.get('size')
    color = request.POST.get('color')


    if not san_pham_id or not size or not color:
        messages.error(request, 'Lỗi: Vui lòng chọn đầy đủ Size và Màu sắc.')
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    
    try:
        so_luong = int(request.POST.get('so_luong', 1))
        if so_luong <= 0: 
            so_luong = 1
    except ValueError:
        so_luong = 1

    try:
        san_pham = SanPham.objects.get(id=san_pham_id)
    except SanPham.DoesNotExist:
        messages.error(request, 'Lỗi: Sản phẩm này không tồn tại.')
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    product_key = f"{san_pham_id}_{size}_{color}"

    if request.user.is_authenticated:
        gio_hang, _ = GioHang.objects.get_or_create(ma_nguoi_dung=request.user)
        
        chi_tiet, created = ChiTietGioHang.objects.get_or_create(
            ma_gio_hang=gio_hang,
            ma_san_pham=san_pham,
            size=size,
            color=color
        )
        
        if not created:
            chi_tiet.so_luong += so_luong # Cộng dồn số lượng
        else:
            chi_tiet.so_luong = so_luong # Tạo mới
        
        chi_tiet.save()

    else:
        gio_hang_session = request.session.get('giohang', {})
        
        if product_key in gio_hang_session:
            gio_hang_session[product_key]['so_luong'] += so_luong
        else:
            # Lưu cả thông tin chi tiết
            gio_hang_session[product_key] = {
                'san_pham_id': san_pham_id,
                'size': size,
                'color': color,
                'so_luong': so_luong
            }

        request.session['giohang'] = gio_hang_session

    messages.success(request, f'Đã thêm "{san_pham.ten_san_pham} ({size}, {color})" vào giỏ hàng.')
    return redirect('gio_hang_view')

def gio_hang_view(request):
    chi_tiet_gio_hang_list = []
    tong_tien = 0
    shipping_fee = 0  # Phí ship cố định (ví dụ)

    if request.user.is_authenticated:
        # Lấy giỏ hàng từ database
        try:
            gio_hang = GioHang.objects.get(ma_nguoi_dung=request.user)
            # Queryset đã có sẵn mọi thứ
            chi_tiet_gio_hang_list = ChiTietGioHang.objects.filter(ma_gio_hang=gio_hang)
            
            for item in chi_tiet_gio_hang_list:
                # Dùng property @property đã định nghĩa trong models.py
                tong_tien += item.tong_tien_item 
        
        except GioHang.DoesNotExist:
            chi_tiet_gio_hang_list = []

    else:
        # Lấy giỏ hàng từ session (LOGIC ĐÃ THAY ĐỔI)
        gio_hang_session = request.session.get('giohang', {})
        
        # key bây giờ là "1_XL_Red"
        for product_key, item_details in gio_hang_session.items():
            try:
                san_pham_id = item_details['san_pham_id']
                so_luong = item_details['so_luong']
                
                san_pham = SanPham.objects.get(id=int(san_pham_id))
                
                gia_san_pham = san_pham.giakm if san_pham.giakm is not None else 0
                tong_tien_item = gia_san_pham * so_luong
                tong_tien += tong_tien_item
                
                chi_tiet_gio_hang_list.append({
                    'id_session_key': product_key, # Gửi key này để xóa/cập nhật
                    'ma_san_pham': san_pham,
                    'so_luong': so_luong,
                    'size': item_details['size'],
                    'color': item_details['color'],
                    'tong_tien_item': tong_tien_item,
                })
            except (SanPham.DoesNotExist, ValueError, KeyError):
                continue

    thanh_tien = tong_tien + shipping_fee
    menudanhmuc = DanhMuc.objects.filter(trang_thai=True)

    context = {
        'menudanhmuc': menudanhmuc,
        'chi_tiet_gio_hang': chi_tiet_gio_hang_list,
        'tong_tien': tong_tien, 
        'shipping_fee': shipping_fee,
        'thanh_tien': thanh_tien, 
    }
    return render(request, 'cart.html', context)

@require_POST
def quan_ly_gio_hang(request):
    item_id = request.POST.get('item_id') # Đây là 'id' (DB) hoặc 'id_session_key' (Session)
    action = request.POST.get('action') # 'increase', 'decrease', 'remove'

    if not item_id or not action:
        messages.error(request, 'Yêu cầu không hợp lệ.')
        return redirect('gio_hang_view')

    if request.user.is_authenticated:
        try:
            # item_id ở đây là ChiTietGioHang.id
            chi_tiet = ChiTietGioHang.objects.get(id=item_id, ma_gio_hang__ma_nguoi_dung=request.user)
            
            if action == 'increase':
                chi_tiet.so_luong += 1
                chi_tiet.save()
                messages.success(request, 'Đã tăng số lượng.')
            
            elif action == 'decrease':
                chi_tiet.so_luong -= 1
                if chi_tiet.so_luong <= 0:
                    chi_tiet.delete() # Xóa nếu về 0
                    messages.success(request, 'Đã xóa sản phẩm.')
                else:
                    chi_tiet.save()
                    messages.success(request, 'Đã giảm số lượng.')
            
            elif action == 'remove':
                chi_tiet.delete()
                messages.success(request, 'Đã xóa sản phẩm.')
        
        except ChiTietGioHang.DoesNotExist:
            messages.error(request, 'Không tìm thấy sản phẩm.')
    
    else:
       
        gio_hang_session = request.session.get('giohang', {})
        
        if item_id not in gio_hang_session:
            messages.error(request, 'Không tìm thấy sản phẩm.')
            return redirect('gio_hang_view')

        if action == 'increase':
            gio_hang_session[item_id]['so_luong'] += 1
            messages.success(request, 'Đã tăng số lượng.')
        
        elif action == 'decrease':
            gio_hang_session[item_id]['so_luong'] -= 1
            if gio_hang_session[item_id]['so_luong'] <= 0:
                del gio_hang_session[item_id] # Xóa nếu về 0
                messages.success(request, 'Đã xóa sản phẩm.')
            else:
                messages.success(request, 'Đã giảm số lượng.')
        
        elif action == 'remove':
            del gio_hang_session[item_id]
            messages.success(request, 'Đã xóa sản phẩm.')
        
        request.session['giohang'] = gio_hang_session

    return redirect('gio_hang_view')