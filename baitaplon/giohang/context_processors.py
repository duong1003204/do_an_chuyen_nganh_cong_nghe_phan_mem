from .models import GioHang, ChiTietGioHang
from django.db.models import Sum

def cart_context(request):
    """
    Cung cấp biến 'cart_total_items' cho TẤT CẢ các template.
    """
    cart_total_items = 0

    if request.user.is_authenticated:
        try:
            gio_hang_db = GioHang.objects.get(ma_nguoi_dung=request.user)
            
            result = ChiTietGioHang.objects.filter(ma_gio_hang=gio_hang_db).aggregate(
                total_quantity=Sum('so_luong')
            )
            
            cart_total_items = result.get('total_quantity') or 0
            
        except GioHang.DoesNotExist:
            cart_total_items = 0
            
    else:
        gio_hang_session = request.session.get('giohang', {})
        

        cart_total_items = sum(item.get('so_luong', 0) for item in gio_hang_session.values())

    return {
        'cart_total_items': cart_total_items
    }