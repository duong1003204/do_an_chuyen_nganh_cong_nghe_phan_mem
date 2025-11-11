from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
import hmac
import hashlib
import urllib.parse
import requests
import json
from datetime import datetime
import pytz # Thêm import pytz

# Import các models
from giohang.models import GioHang, ChiTietGioHang
from .models import DonHang, ChiTietDonHang

# --- CẤU HÌNH VNPAY DEMO ---
# (Lấy từ Sandbox của VNPAY)
VNPAY_TMNCODE = "BTQM0MAO" # Mã website
VNPAY_HASH_SECRET_KEY = "4TYACLKZ3JHF73VO5QCLQXZXJS9WMTZM" # Mã bí mật
VNPAY_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html" # URL thanh toán
VNPAY_RETURN_URL = 'http://127.0.0.1:8000/donhang/vnpay_return/' # URL VNPAY gọi về (phải khớp với urls.py)


# --- 1. VIEW HIỂN THỊ TRANG CHECKOUT ---
@login_required
def checkout_view(request):
    # Lấy giỏ hàng của người dùng
    try:
        gio_hang_db = GioHang.objects.get(ma_nguoi_dung=request.user)
        cart_items = ChiTietGioHang.objects.filter(ma_gio_hang=gio_hang_db)
        
        if not cart_items.exists():
            messages.error(request, "Giỏ hàng của bạn đang trống.")
            return redirect('gio_hang_view')
            
    except GioHang.DoesNotExist:
        messages.error(request, "Giỏ hàng của bạn đang trống.")
        return redirect('gio_hang_view')

    # Tính toán tổng tiền
    subtotal = 0
    for item in cart_items:
        subtotal += item.tong_tien_item # Dùng property 'tong_tien_item' từ model
    
    shipping_fee = 10 # Phí ship (ví dụ)
    total = subtotal + shipping_fee

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total': total,
        'user': request.user # Gửi thông tin user để điền form
    }
    return render(request, 'checkout.html', context)


# --- 2. VIEW XỬ LÝ ĐẶT HÀNG (COD & VNPAY) ---
@login_required
def place_order_view(request):
    if request.method == 'POST':
        # Lấy thông tin từ form
        ho_ten = request.POST.get('ho_ten')
        email = request.POST.get('email')
        so_dien_thoai = request.POST.get('so_dien_thoai')
        dia_chi = request.POST.get('dia_chi_giao') # Tên trường này phải khớp form
        payment_method = request.POST.get('payment_method') # Tên trường này phải khớp form
        ghi_chu = request.POST.get('ghi_chu', '') # Thêm trường ghi chú (nếu có)

        # Lấy lại giỏ hàng và tính lại tổng tiền (để bảo mật)
        try:
            gio_hang_db = GioHang.objects.get(ma_nguoi_dung=request.user)
            cart_items = ChiTietGioHang.objects.filter(ma_gio_hang=gio_hang_db)
            if not cart_items.exists():
                messages.error(request, "Giỏ hàng trống, không thể đặt hàng.")
                return redirect('gio_hang_view')
        except GioHang.DoesNotExist:
            messages.error(request, "Lỗi giỏ hàng.")
            return redirect('gio_hang_view')

        subtotal = 0
        for item in cart_items:
            subtotal += item.tong_tien_item
        shipping_fee = 10
        total = subtotal + shipping_fee
        
        # --- Tạo Đơn Hàng ---
        try:
            don_hang = DonHang.objects.create(
                ma_nguoi_dung=request.user,
                tong_tien=total,
                dia_chi_giao=dia_chi,
                phuong_thuc_thanh_toan=payment_method,
                trang_thai_don_hang='cho_xu_ly', # Trạng thái ban đầu
                ghi_chu=ghi_chu
            )

            # Chuyển sản phẩm từ giỏ hàng sang Chi Tiết Đơn Hàng
            for item in cart_items:
                ChiTietDonHang.objects.create(
                    ma_don_hang=don_hang,
                    ma_san_pham=item.ma_san_pham,
                    so_luong=item.so_luong,
                    gia=item.ma_san_pham.giakm, # Lưu giá tại thời điểm mua
                    thanh_tien=item.tong_tien_item # Lưu thành tiền
                )
            
            # Xóa giỏ hàng (ChiTietGioHang)
            cart_items.delete()

            # --- Xử lý phương thức thanh toán ---
            if payment_method == 'cod':
                # (Thanh toán khi nhận hàng)
                messages.success(request, 'Đặt hàng COD thành công!')
                return redirect('order_success', order_id=don_hang.id)

            elif payment_method == 'vnpay':
                # (Thanh toán VNPAY)
                # Chuyển hướng đến VNPAY
                
                # Cài đặt múi giờ Việt Nam
                vnp_CreateDate = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%Y%m%d%H%M%S')
                vnp_Amount = int(total * 100) # VNPAY yêu cầu số nguyên (nhân 100)
                vnp_OrderInfo = f"Thanh toan don hang {don_hang.id}"
                vnp_TxnRef = str(don_hang.id) # Mã đơn hàng của bạn
                vnp_IpAddr = request.META.get('REMOTE_ADDR')

                input_data = {
                    "vnp_Version": "2.1.0",
                    "vnp_Command": "pay",
                    "vnp_TmnCode": VNPAY_TMNCODE,
                    "vnp_Amount": vnp_Amount,
                    "vnp_CreateDate": vnp_CreateDate,
                    "vnp_CurrCode": "VND",
                    "vnp_IpAddr": vnp_IpAddr,
                    "vnp_Locale": "vn",
                    "vnp_OrderInfo": vnp_OrderInfo,
                    "vnp_OrderType": "other",
                    "vnp_ReturnUrl": VNPAY_RETURN_URL,
                    "vnp_TxnRef": vnp_TxnRef,
                }
                
                # Sắp xếp data
                input_data = dict(sorted(input_data.items()))
                
                # Tạo query string
                query_string = urllib.parse.urlencode(input_data, safe="%")
                
                # Tạo hash
                hash_data = VNPAY_HASH_SECRET_KEY + "&" + query_string
                secure_hash = hmac.new(
                    VNPAY_HASH_SECRET_KEY.encode(), 
                    query_string.encode(), 
                    hashlib.sha512
                ).hexdigest()
                
                # URL thanh toán cuối cùng
                payment_url = VNPAY_URL + "?" + query_string + "&vnp_SecureHash=" + secure_hash
                
                return HttpResponseRedirect(payment_url)

        except Exception as e:
            messages.error(request, f"Đã xảy ra lỗi khi tạo đơn hàng: {e}")
            return redirect('checkout')

    messages.error(request, "Yêu cầu không hợp lệ.")
    return redirect('checkout')


# --- 3. VIEW XỬ LÝ KẾT QUẢ VNPAY TRẢ VỀ ---
def vnpay_return_view(request):
    # Lấy dữ liệu VNPAY trả về
    input_data = request.GET.dict()
    
    if input_data:
        vnp_SecureHash = input_data.pop('vnp_SecureHash', '')
        
        # Sắp xếp lại dữ liệu
        input_data = dict(sorted(input_data.items()))
        
        # Tạo query string
        query_string = urllib.parse.urlencode(input_data, safe="%")
        
        # Tạo hash mới
        hash_data = VNPAY_HASH_SECRET_KEY + "&" + query_string
        new_secure_hash = hmac.new(
            VNPAY_HASH_SECRET_KEY.encode(), 
            query_string.encode(), 
            hashlib.sha512
        ).hexdigest()
        
        # Lấy mã đơn hàng
        order_id = input_data.get('vnp_TxnRef', None)
        try:
            don_hang = DonHang.objects.get(id=order_id)
        except DonHang.DoesNotExist:
            messages.error(request, "Lỗi: Không tìm thấy đơn hàng.")
            return redirect('index') # Về trang chủ

        # --- KIỂM TRA HASH (Quan trọng) ---
        if new_secure_hash == vnp_SecureHash:
            vnp_ResponseCode = input_data.get('vnp_ResponseCode', None)
            
            # --- THANH TOÁN THÀNH CÔNG ---
            if vnp_ResponseCode == '00':
                messages.success(request, f"Thanh toán VNPAY thành công cho đơn hàng #{order_id}!")
                return redirect('order_success', order_id=don_hang.id)
            
            # --- THANH TOÁN THẤT BẠI (hoặc bị hủy) ---
            else:
                # Cập nhật trạng thái đơn hàng là đã hủy
                don_hang.trang_thai_don_hang = 'da_huy'
                don_hang.save()
                
                # (Bạn có thể thêm logic hoàn trả sản phẩm vào giỏ hàng ở đây nếu muốn)
                
                messages.error(request, f"Thanh toán VNPAY thất bại (Mã lỗi: {vnp_ResponseCode}). Đơn hàng #{order_id} đã bị hủy.")
                return redirect('gio_hang_view') # Quay lại giỏ hàng
        
        # --- LỖI SAI HASH ---
        else:
            messages.error(request, "Lỗi bảo mật: Chữ ký VNPAY không hợp lệ.")
            don_hang.trang_thai_don_hang = 'da_huy' # Hủy đơn hàng nếu hash sai
            don_hang.save()
            return redirect('gio_hang_view')
            
    messages.error(request, "Không nhận được dữ liệu trả về từ VNPAY.")
    return redirect('gio_hang_view')


# --- 4. VIEW ĐẶT HÀNG THÀNH CÔNG ---
@login_required
def order_success_view(request, order_id):
    try:
        order = DonHang.objects.get(id=order_id, ma_nguoi_dung=request.user)
    except DonHang.DoesNotExist:
        messages.error(request, "Không tìm thấy đơn hàng.")
        return redirect('index')
        
    context = {
        'order': order
    }
    return render(request, 'order_success.html', context)