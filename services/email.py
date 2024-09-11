from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from equi_media_portal import settings


def send_contact_email_message(subject, email, content, ip, user_id):
    """
    Function to send contact form email
    """
    user = User.objects.get(id=user_id) if user_id else None
    message = render_to_string('portal/email/feedback_email_send.html', {
        'email': email,
        'content': content,
        'ip': ip,
        'user': user,
    })
    email = EmailMessage(subject, message, settings.SERVER_EMAIL, [settings.EMAIL_ADMIN])
    email.send(fail_silently=False)


def send_testimonial_email_message(subject, email, content, ip, author):
    """
    Function to send testimonial form email
    """
    message = render_to_string('testimonial/email/testimonial_email_send.html', {
        'email': email,
        'content': content,
        'ip': ip,
        'user': author,
    })
    email = EmailMessage(subject, message, settings.SERVER_EMAIL, [settings.EMAIL_ADMIN])
    email.send(fail_silently=False)
