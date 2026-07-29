import logging
import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)


def _send_email_task(booking):
    """
    Worker function executed in a background thread to send email without blocking HTTP responses.
    """
    if not booking.email:
        logger.warning(f"Booking #{booking.id} has no email address.")
        return

    subject = f"Booking Confirmed — Knead Hushed Massage (Appointment #{booking.id})"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Knead Hushed Massage <bookings@kneadhushedmassage.com>')
    to_email = [booking.email]

    text_content = f"""Dear {booking.first_name},

Great news! Your booking with Knead Hushed Massage has been officially approved and confirmed.

BOOKING DETAILS:
------------------------------------------
Appointment Reference: #{booking.id}
Service: {booking.service}
Duration: {booking.duration}
Date: {booking.appointment_date}
Time Slot: {booking.appointment_time}
Phone: {booking.phone}
------------------------------------------

IMPORTANT PAYMENT INSTRUCTIONS:
Please reply directly to this email to proceed with payment and finalize your reservation.

We look forward to welcoming you for a truly relaxing experience.

Warm regards,
Knead Hushed Massage Team
www.kneadhushedmassage.com
"""

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: #2c3e50;
      line-height: 1.6;
      background-color: #f8f9fa;
      margin: 0;
      padding: 20px;
    }}
    .email-container {{
      max-width: 580px;
      margin: 0 auto;
      background: #ffffff;
      padding: 32px 28px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }}
    .header-title {{
      color: #8A9A5B;
      font-size: 22px;
      font-weight: 700;
      margin-top: 0;
      margin-bottom: 16px;
    }}
    .details-box {{
      background: #fdfdfd;
      border: 1px solid #edf2f7;
      border-left: 4px solid #8A9A5B;
      padding: 16px 20px;
      margin: 20px 0;
      border-radius: 4px;
    }}
    .details-row {{
      margin-bottom: 8px;
      font-size: 14px;
    }}
    .details-row strong {{
      color: #4a5568;
    }}
    .action-callout {{
      background: #f0f4e4;
      border: 1px solid #d1dfab;
      color: #4a5d23;
      padding: 16px;
      border-radius: 6px;
      font-weight: 600;
      margin: 24px 0;
      text-align: center;
      font-size: 15px;
    }}
    .footer {{
      margin-top: 30px;
      padding-top: 18px;
      border-top: 1px solid #edf2f7;
      font-size: 13px;
      color: #718096;
      text-align: center;
    }}
    .footer a {{
      color: #8A9A5B;
      text-decoration: none;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="email-container">
    <h2 class="header-title">Booking Confirmed!</h2>
    <p>Dear <strong>{booking.first_name}</strong>,</p>
    <p>We are pleased to inform you that your appointment with <strong>Knead Hushed Massage</strong> has been approved and confirmed.</p>
    
    <div class="details-box">
      <div class="details-row"><strong>Appointment Reference:</strong> #{booking.id}</div>
      <div class="details-row"><strong>Service:</strong> {booking.service}</div>
      <div class="details-row"><strong>Duration:</strong> {booking.duration}</div>
      <div class="details-row"><strong>Date:</strong> {booking.appointment_date}</div>
      <div class="details-row"><strong>Time Slot:</strong> {booking.appointment_time}</div>
      <div class="details-row"><strong>Contact Phone:</strong> {booking.phone}</div>
    </div>

    <div class="action-callout">
      👉 Please reply directly to this email to proceed with payment and finalize your reservation.
    </div>

    <p>If you have any special requests or questions prior to your session, simply reply to this email.</p>

    <div class="footer">
      <p style="margin: 0 0 4px 0;"><strong>Knead Hushed Massage</strong></p>
      <p style="margin: 0;"><a href="https://www.kneadhushedmassage.com">www.kneadhushedmassage.com</a> | Your Wellness Adventure Begins Here</p>
    </div>
  </div>
</body>
</html>
"""

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
        logger.info(f"Confirmation email sent to {booking.email} for Booking #{booking.id}")
    except BaseException as e:
        logger.error(
            f"Failed to send confirmation email to {booking.email} for Booking #{booking.id}: {type(e).__name__}: {e}",
            exc_info=True
        )


def send_booking_confirmation_email(booking):
    """
    Launches email sending in a non-blocking background thread.
    This guarantees Django Admin responds instantly and prevents Gunicorn worker timeout 500 errors.
    """
    try:
        thread = threading.Thread(target=_send_email_task, args=(booking,), daemon=True)
        thread.start()
        return True
    except BaseException as e:
        logger.error(f"Error starting email thread for Booking #{booking.id}: {e}")
        return False
