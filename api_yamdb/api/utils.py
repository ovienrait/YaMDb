from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

token_generator = PasswordResetTokenGenerator()


def generate_confirmation_code(user):
    return token_generator.make_token(user)


def check_confirmation_code(user, token):
    return token_generator.check_token(user, token)


def send_email_confirmation_code(email, confirmation_code):
    send_mail(
        'Your confirmation code',
        f'Your confirmation code is: {confirmation_code}',
        'from@example.com',
        [email],
        fail_silently=False,
    )
