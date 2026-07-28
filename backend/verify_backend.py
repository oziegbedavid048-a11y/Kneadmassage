import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knead_backend.settings')
django.setup()

from bookings.models import Booking

# Create test booking
test_booking = Booking.objects.create(
    first_name="Ashley",
    last_name="Taylor",
    email="ashley.test@example.com",
    phone="5552345678",
    zipcode="90210",
    service="Deep Tissue Massage",
    duration="90 mins",
    appointment_date="2026-08-01",
    appointment_time="02:00 PM",
    hear_about="Instagram",
    notes="Prefers firm pressure on lower back",
    status="Pending"
)

print(f"VERIFICATION SUCCESS: Created test booking -> {test_booking}")
print(f"Total bookings in DB: {Booking.objects.count()}")
