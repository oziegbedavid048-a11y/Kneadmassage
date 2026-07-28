from django.urls import path
from . import views

urlpatterns = [
    path('bookings/create/', views.submit_booking, name='submit_booking'),
    path('bookings/', views.list_bookings, name='list_bookings'),
]
