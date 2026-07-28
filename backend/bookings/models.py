from django.db import models


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    SERVICE_CHOICES = [
        ('Nuru Massage', 'Nuru Massage'),
        ('Swedish Massage', 'Swedish Massage'),
        ('Deep Tissue Massage', 'Deep Tissue Massage'),
        ('Lingam Massage', 'Lingam Massage'),
        ('Lymphatic Drainage', 'Lymphatic Drainage'),
        ('Thai Massage', 'Thai Massage'),
        ('Tantric Massage', 'Tantric Massage'),
        ('Ashiatsu Massage', 'Ashiatsu Massage'),
        ('Jacuzzi Treatment', 'Jacuzzi Treatment'),
        ('Massage & Happy Ending', 'Massage & Happy Ending'),
    ]

    # Customer Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)

    # Booking Details
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    duration = models.CharField(max_length=50)
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=50)
    
    # Additional Info
    hear_about = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # Admin Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"Booking #{self.id} - {self.full_name} ({self.service} on {self.appointment_date})"
