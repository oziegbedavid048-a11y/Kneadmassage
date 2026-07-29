import logging
from django.contrib import admin, messages
from .models import Booking
from .emails import send_booking_confirmation_email

logger = logging.getLogger(__name__)


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

    def _try_send_confirmation_email(self, request, booking):
        """
        Safely attempt to send a confirmation email.
        Never raises — logs errors and shows admin messages instead.
        """
        try:
            sent = send_booking_confirmation_email(booking)
            if sent:
                self.message_user(
                    request,
                    f"✅ Confirmation email sent to {booking.email} for Booking #{booking.id}.",
                    messages.SUCCESS
                )
            else:
                self.message_user(
                    request,
                    f"⚠️ Booking #{booking.id} confirmed, but the email to {booking.email} could not be sent. Check your ZeptoMail settings.",
                    messages.WARNING
                )
        except Exception as exc:
            logger.error(f"Email send failed for Booking #{booking.id}: {exc}", exc_info=True)
            self.message_user(
                request,
                f"⚠️ Booking #{booking.id} status saved as Confirmed, but email failed: {exc}. Check Render logs and ZeptoMail credentials.",
                messages.WARNING
            )

    def save_model(self, request, obj, form, change):
        """
        Detect when status changes to Confirmed on the detail page and send email.
        Errors in email sending are caught and shown as admin warnings — never 500.
        """
        old_status = None
        if change and obj.pk:
            try:
                old_obj = Booking.objects.filter(pk=obj.pk).first()
                if old_obj:
                    old_status = old_obj.status
            except Exception:
                pass

        super().save_model(request, obj, form, change)

        # Send confirmation email only if status just changed TO Confirmed
        if obj.status == 'Confirmed' and old_status != 'Confirmed':
            self._try_send_confirmation_email(request, obj)

    def save_formset(self, request, form, formset, change):
        """
        Handle inline list-editable saves (status changed from the changelist table).
        Detect Confirmed transitions and send emails safely.
        """
        # Capture old statuses before saving
        old_statuses = {}
        for form_instance in formset.forms:
            obj = form_instance.instance
            if obj.pk:
                try:
                    old_obj = Booking.objects.filter(pk=obj.pk).first()
                    if old_obj:
                        old_statuses[obj.pk] = old_obj.status
                except Exception:
                    pass

        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
            old_status = old_statuses.get(instance.pk)
            if instance.status == 'Confirmed' and old_status != 'Confirmed':
                self._try_send_confirmation_email(request, instance)
        formset.save_m2m()

    @admin.action(description='✅ Mark selected as Confirmed & Send Confirmation Email')
    def mark_confirmed(self, request, queryset):
        count = 0
        for booking in queryset:
            if booking.status != 'Confirmed':
                booking.status = 'Confirmed'
                booking.save()
                count += 1
                self._try_send_confirmation_email(request, booking)
        if count == 0:
            self.message_user(request, "All selected bookings were already Confirmed.", messages.WARNING)
        else:
            self.message_user(request, f"Marked {count} booking(s) as Confirmed.", messages.SUCCESS)

    @admin.action(description='Mark selected bookings as Completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='Completed')
        self.message_user(request, "Selected booking(s) marked as Completed.", messages.SUCCESS)

    @admin.action(description='Mark selected bookings as Cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
        self.message_user(request, "Selected booking(s) marked as Cancelled.", messages.SUCCESS)
