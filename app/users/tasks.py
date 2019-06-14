from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery.decorators import task


@task(name="user_verification_task")
def user_verification_task(url, user_email):
    context = {
        'url': url
    }
    send_mail(
            subject='Verification Mail',
            message=render_to_string('verificationTemplate.txt', context),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=render_to_string('verificationTemplate.html', context),
            fail_silently=False,
        )


@task(name="send_friend_request_task")
def send_friend_request_task(url, sending_user, recipient_email, user_name):
    context = {
        'user_name': user_name,
        'url': url
    }
    send_mail(
            subject='Follow Request',
            message=render_to_string('friendRequestTemplate.txt', context),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            html_message=render_to_string('friendRequestTemplate.html', context),
            fail_silently=False,
        )
