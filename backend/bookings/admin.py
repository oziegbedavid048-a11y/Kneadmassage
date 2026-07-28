from django.contrib import admin, messages
from .models import Booking
from .emails import send_booking_confirmation_email


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

    def save_model(self, request, obj, form, change):
        old_status = None
        if change and obj.pk:
            old_obj = Booking.objects.filter(pk=obj.pk).first()
            if old_obj:
                old_status = old_obj.status

        super().save_model(request, obj, form, change)

        # If status changed to Confirmed, send confirmation email
        if obj.status == 'Confirmed' and old_status != 'Confirmed':
            sent = send_booking_confirmation_email(obj)
            if sent:
                self.message_user(request, f"Confirmation email sent to {obj.email} for Booking #{obj.id}.", messages.SUCCESS)
            else:
                self.message_user(request, f"Booking #{obj.id} confirmed, but failed to send email to {obj.email}. Check logs.", messages.WARNING)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            old_status = None
            if instance.pk:
                old_obj = Booking.objects.filter(pk=instance.pk).first()
                if old_obj:
                    old_status = old_obj.status
            instance.save()
            if instance.status == 'Confirmed' and old_status != 'Confirmed':
                sent = send_booking_confirmation_email(instance)
                if sent:
                    self.message_user(request, f"Confirmation email sent to {instance.email} for Booking #{instance.id}.", messages.SUCCESS)
                else:
                    self.message_user(request, f"Booking #{instance.id} confirmed, but email sending failed.", messages.WARNING)
        formset.save_m2m()

    @admin.action(description='Mark selected bookings as Confirmed & Send Email')
    def mark_confirmed(self, request, queryset):
        count = 0
        email_count = 0
        for booking in queryset:
            if booking.status != 'Confirmed':
                booking.status = 'Confirmed'
                booking.save()
                count += 1
                sent = send_booking_confirmation_email(booking)
                if sent:
                    email_count += 1
        self.message_user(request, f"Marked {count} booking(s) as Confirmed. {email_count} confirmation email(s) sent successfully.", messages.SUCCESS)

    @admin.action(description='Mark selected bookings as Completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='Completed')
        self.message_user(request, "Selected booking(s) marked as Completed.", messages.SUCCESS)

    @admin.action(description='Mark selected bookings as Cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
        self.message_user(request, "Selected booking(s) marked as Cancelled.", messages.SUCCESS)
