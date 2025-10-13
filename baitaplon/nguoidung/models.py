
from django.contrib.auth.models import AbstractUser
from django.db import models

class NguoiDung(AbstractUser):
    ho_ten = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=20, blank=True, null=True)
    dia_chi = models.CharField(max_length=255, blank=True, null=True)
    trang_thai = models.BooleanField(default=True)

    def __str__(self):
        return self.ho_ten or self.username
