from django.core.mail import send_mail
from emails.interfaces import EmailServiceInterface

class DjangoSMTPEmailService(EmailServiceInterface):
    def send_email(self, to, subject, body):
        send_mail(
            subject=subject,
            message=body,
            from_email=None,
            recipient_list=[to],
            fail_silently=False,
        )
        return {
            "to": to,
            "subject": subject,
            "status": "sent_smtp",
        }
