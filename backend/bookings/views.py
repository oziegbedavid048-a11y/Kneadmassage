import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Booking


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

        first_name = data.get('first_name') or data.get('firstName') or ''
        last_name = data.get('last_name') or data.get('lastName') or ''
        email = data.get('email') or ''
        phone = data.get('phone') or ''
        zipcode = data.get('zipcode') or ''
        service = data.get('service') or ''
        duration = data.get('duration') or ''
        appointment_date = data.get('appointment_date') or data.get('appointmentDate') or ''
        appointment_time = data.get('appointment_time') or data.get('appointmentTime') or ''
        hear_about = data.get('hear_about') or data.get('hearAbout') or ''
        notes = data.get('notes') or ''

        # Basic validation
        if not all([first_name, email, phone, service, appointment_date, appointment_time]):
            response = JsonResponse({
                'success': False,
                'error': 'Missing required fields. Please complete all required fields.'
            }, status=400)
            response["Access-Control-Allow-Origin"] = "*"
            return response

        booking = Booking.objects.create(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            email=email.strip(),
            phone=phone.strip(),
            zipcode=zipcode.strip(),
            service=service.strip(),
            duration=duration.strip(),
            appointment_date=appointment_date.strip(),
            appointment_time=appointment_time.strip(),
            hear_about=hear_about.strip(),
            notes=notes.strip(),
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
        response = JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
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
