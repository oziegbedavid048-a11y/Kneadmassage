from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name_display',
        'email',
        'phone',
        'service',
        'appointment_date',
        'appointment_time',
        'duration',
        'status',
        'created_at',
    )
    
    list_display_links = ('id', 'full_name_display')
    
    # Enable direct editing of status from the admin table view
    list_editable = ('status',)

    list_filter = ('status', 'service', 'appointment_date', 'created_at')

    search_fields = ('first_name', 'last_name', 'email', 'phone', 'zipcode', 'notes')

    date_hierarchy = 'appointment_date'

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Customer Information', {
            'fields': (('first_name', 'last_name'), ('email', 'phone'), 'zipcode')
        }),
        ('Appointment Details', {
            'fields': (('service', 'duration'), ('appointment_date', 'appointment_time'))
        }),
        ('Customer Notes & Source', {
            'fields': ('hear_about', 'notes')
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    @admin.display(description='Customer Name')
    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.action(description='Mark selected bookings as Confirmed')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='Confirmed')

    @admin.action(description='Mark selected bookings as Completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='Completed')

    @admin.action(description='Mark selected bookings as Cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
