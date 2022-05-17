from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from six import text_type


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.username) + text_type(timestamp) + text_type(user.last_login)


token_generator = AppTokenGenerator()


def send_email(email_subject, email_body, to, msg_type='text'):
    if not to:
        return
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
    )
    if msg_type == 'html':
        email.content_subtype = 'html'
    email.send(fail_silently=False)


def send_email_token(user, domain, url_part, email_subject, email_body):
    user_id = urlsafe_base64_encode(force_bytes(user.username))
    token = token_generator.make_token(user)
    relative = reverse(url_part, kwargs={'user_id': user_id,
                                         'token': token})
    activate_url = f'http://{domain}{relative}'

    send_email(email_subject, email_body.format(user.username, activate_url), [user.email])
