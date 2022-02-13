from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('send-otp/', send_otp),
    path('verify-otp/', verify_otp),
    path('resend-otp/', resend_otp),
    path('admin/', admin.site.urls),
]
