import json
import logging
import threading
import urllib.request
import urllib.error
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)


def _send_via_zeptomail_api(booking, subject, text_content, html_content):
    """
    Sends email directly via ZeptoMail REST API over HTTPS (Port 443).
    Bypasses SMTP port 587/2525 blocks imposed by cloud hosts like Render.
    """
    token = getattr(settings, 'EMAIL_HOST_PASSWORD', '').strip()
    if not token:
        return False

    url = "https://api.zeptomail.com/v1.1/email"
    
    # Payload as required by ZeptoMail API v1.1
    payload = {
        "from": {
            "address": "bookings@kneadhushedmassage.com",
            "name": "Knead Hushed Massage"
        },
        "to": [
            {
                "email_address": {
                    "address": booking.email,
                    "name": booking.first_name or "Valued Customer"
                }
            }
        ],
        "subject": subject,
        "htmlbody": html_content,
        "textbody": text_content
    }

    data = json.dumps(payload).encode('utf-8')

    # Try both valid ZeptoMail Authorization header formats (zoho-enczapikey and SendMailToken)
    auth_headers = [
        f"zoho-enczapikey {token}",
        f"SendMailToken {token}",
        token  # Raw token format if passed directly
    ]

    for auth_val in auth_headers:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": auth_val
        }
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                resp_body = response.read().decode('utf-8')
                logger.info(f"SUCCESS: Confirmation email sent via ZeptoMail HTTPS API for Booking #{booking.id}: {resp_body}")
                return True
        except urllib.error.HTTPError as err:
            err_msg = err.read().decode('utf-8') if err.fp else str(err)
            logger.warning(f"ZeptoMail HTTPS API HTTP {err.code} with header '{auth_val[:20]}...': {err_msg}")
        except BaseException as err:
            logger.warning(f"ZeptoMail HTTPS API error with header '{auth_val[:20]}...': {err}")

    return False


def _send_email_task(booking):
    """
    Worker function executed in a background thread.
    1. Tries ZeptoMail HTTPS REST API (Port 443 — 100% unblocked on Render).
    2. Fallback to standard Django SMTP if HTTPS API does not complete.
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

    # Primary Attempt: HTTPS REST API (Port 443 — NEVER blocked by Render)
    api_success = _send_via_zeptomail_api(booking, subject, text_content, html_content)
    if api_success:
        return

    # Secondary Fallback Attempt: Standard Django SMTP
    logger.info(f"HTTPS API attempt did not complete. Falling back to Django SMTP for Booking #{booking.id}...")
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        sent_count = msg.send(fail_silently=False)
        if sent_count > 0:
            logger.info(f"SUCCESS: Confirmation email sent via SMTP to {booking.email} for Booking #{booking.id}")
        else:
            logger.error(f"FAILURE: SMTP email send returned 0 for Booking #{booking.id}")
    except BaseException as e:
        logger.error(
            f"EXCEPTIONAL SMTP FAILURE sending email to {booking.email} for Booking #{booking.id}: {type(e).__name__}: {e}",
            exc_info=True
        )


def send_booking_confirmation_email(booking):
    """
    Launches email sending in a non-blocking background thread.
    This guarantees Django Admin responds instantly.
    """
    try:
        thread = threading.Thread(target=_send_email_task, args=(booking,), daemon=True)
        thread.start()
        return True
    except BaseException as e:
        logger.error(f"Error starting email thread for Booking #{booking.id}: {e}")
        return False
