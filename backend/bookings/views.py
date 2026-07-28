import json
import logging
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Booking

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def submit_booking(request):
    if request.method == "OPTIONS":
        response = JsonResponse({'status': 'ok'})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Accept"
        return response

    try:
        data = {}
        if request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except Exception:
                data = request.POST
        else:
            data = request.POST

        first_name = (data.get('first_name') or data.get('firstName') or '').strip()
        last_name = (data.get('last_name') or data.get('lastName') or '').strip()
        email = (data.get('email') or '').strip()
        phone = (data.get('phone') or '').strip()
        zipcode = (data.get('zipcode') or '').strip()
        service = (data.get('service') or '').strip()
        duration = (data.get('duration') or '').strip()
        raw_date = (data.get('appointment_date') or data.get('appointmentDate') or '').strip()
        appointment_time = (data.get('appointment_time') or data.get('appointmentTime') or '').strip()
        hear_about = (data.get('hear_about') or data.get('hearAbout') or '').strip()
        notes = (data.get('notes') or '').strip()

        # Parse appointment_date safely to prevent DateField ValueError crashes
        parsed_date = timezone.now().date()
        if raw_date:
            try:
                parsed_date = datetime.strptime(raw_date, '%Y-%m-%d').date()
            except ValueError:
                try:
                    parsed_date = datetime.strptime(raw_date, '%m/%d/%Y').date()
                except ValueError:
                    pass

        # Fallbacks for mandatory fields
        if not first_name:
            first_name = 'Valued Customer'
        if not service:
            service = 'Massage Therapy Session'
        if not appointment_time:
            appointment_time = '10:00 AM'

        booking = Booking.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            zipcode=zipcode,
            service=service,
            duration=duration,
            appointment_date=parsed_date,
            appointment_time=appointment_time,
            hear_about=hear_about,
            notes=notes,
            status='Pending'
        )

        response = JsonResponse({
            'success': True,
            'booking_id': booking.id,
            'message': 'Your booking request has been submitted successfully!'
        }, status=201)
        response["Access-Control-Allow-Origin"] = "*"
        return response

    except Exception as e:
        logger.error(f"Error creating booking: {e}")
        response = JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@require_http_methods(["GET"])
def list_bookings(request):
    """Optional read API for bookings summary"""
    bookings = Booking.objects.all()[:50]
    data = [
        {
            'id': b.id,
            'name': b.full_name,
            'email': b.email,
            'phone': b.phone,
            'service': b.service,
            'date': str(b.appointment_date),
            'time': b.appointment_time,
            'status': b.status,
            'created_at': b.created_at.strftime('%Y-%m-%d %H:%M'),
        }
        for b in bookings
    ]
    response = JsonResponse({'success': True, 'bookings': data})
    response["Access-Control-Allow-Origin"] = "*"
    return response
