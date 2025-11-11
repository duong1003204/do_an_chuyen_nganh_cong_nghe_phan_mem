from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NguoiDung  # Import model NguoiDung của bạn

class NguoiDungCreationForm(UserCreationForm):
    """
    Đây là Form tùy chỉnh cho việc ĐĂNG KÝ.
    """
    class Meta(UserCreationForm.Meta):
        model = NguoiDung  # Bảo Django dùng model NguoiDung
        
        # Các trường bạn muốn hiển thị trên form đăng ký
        # (username, password1, password2 đã có sẵn)
        fields = ('username', 'ho_ten', 'email', 'so_dien_thoai', 'dia_chi')

class NguoiDungChangeForm(UserChangeForm):
    """
    Đây là Form tùy chỉnh cho trang ADMIN.
    """
    class Meta:
        model = NguoiDung # Bảo Django dùng model NguoiDung
        fields = '__all__' # Hoặc liệt kê các trường bạn muốn