import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Booking


@csrf_exempt
@require_http_methods(["POST"])
def submit_booking(request):
    try:
        # Handle both JSON body and form-encoded data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        first_name = data.get('firstName') or data.get('first_name', '')
        last_name = data.get('lastName') or data.get('last_name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        zipcode = data.get('zipcode', '')
        service = data.get('service', '')
        duration = data.get('duration', '')
        appointment_date = data.get('appointmentDate') or data.get('appointment_date', '')
        appointment_time = data.get('appointmentTime') or data.get('appointment_time', '')
        hear_about = data.get('hearAbout') or data.get('hear_about', '')
        notes = data.get('notes', '')

        # Basic validation
        if not all([first_name, last_name, email, phone, service, appointment_date, appointment_time]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields. Please fill out all required fields.'
            }, status=400)

        booking = Booking.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            zipcode=zipcode,
            service=service,
            duration=duration,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            hear_about=hear_about,
            notes=notes,
            status='Pending'
        )

        return JsonResponse({
            'success': True,
            'booking_id': booking.id,
            'message': 'Your booking request has been submitted successfully!'
        }, status=201)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


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
    return JsonResponse({'success': True, 'bookings': data})
