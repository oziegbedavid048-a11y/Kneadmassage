from django.contrib import admin
from django.urls import path, include

# Customize Django Admin branding
admin.site.site_header = "Knead Hushed Massage Administration"
admin.site.site_title = "Knead Massage Admin Portal"
admin.site.index_title = "Booking & Customer Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bookings.urls')),
]
