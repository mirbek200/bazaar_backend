from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from apps.users.models import MyUser
from django.template.loader import render_to_string


def send_message_chat_notification(recipient_id, sender_id):
    sender = get_object_or_404(MyUser, id=sender_id)
    recipient = get_object_or_404(MyUser, id=recipient_id)
    account = settings.GMAIL_ACCOUNTS[0]
    host = account['EMAIL_HOST_USER']
    password_email = account["EMAIL_HOST_PASSWORD"]
    message = f"Вам отправил собщение {sender.email}"
    send_mail("Chat message", message, host, [recipient.email], auth_user=host, auth_password=password_email)


def send_email_after_ban(user):
    from_email = 'test@gmail.com'
    to_email = [user]

    message = render_to_string('email_after_ban.html')

    send_mail("Was banned", message, from_email, to_email, html_message=message)


def send_email_gift(user):
    from_email = 'test@gmail.com'
    to_email = [user]

    message = render_to_string('gift.html')

    send_mail("КОНКУРС! CONTEST! Post an ad and win 40,000 ฿ at CENTRAL💸", message, from_email, to_email, html_message=message)


def submitted_for_review(email, announcement_id):
    account = settings.GMAIL_ACCOUNTS[0]
    host = account['EMAIL_HOST_USER']
    password_email = account["EMAIL_HOST_PASSWORD"]
    message = render_to_string('for_review.html')
    send_mail("Submitted for review", message, host, [email], auth_user=host, auth_password=password_email, html_message=message)


def ad_published(email, announcement_id):
    account = settings.GMAIL_ACCOUNTS[0]
    host = account['EMAIL_HOST_USER']
    password_email = account["EMAIL_HOST_PASSWORD"]
    context = {
        "id": announcement_id
    }
    message = render_to_string('ad_published.html', context)
    send_mail("Ваше объявление опубликовано | Your ad has been published", message, host, [email], auth_user=host, auth_password=password_email, html_message=message)


def banned_announcement(email, announcement_id):
    account = settings.GMAIL_ACCOUNTS[0]
    host = account['EMAIL_HOST_USER']
    password_email = account["EMAIL_HOST_PASSWORD"]
    message = render_to_string('is_banned.html')
    send_mail("Is banned", message, host, [email], auth_user=host, auth_password=password_email, html_message=message)

def send_email_change_password(user):
    from_email = 'test@gmail.com'
    to_email = [user]
    context = {
        "activation_code": user.activation_code,
        "name": user.full_name,
    }
    message = render_to_string('forgot_password.html', context)

    send_mail("Forgot password", message, from_email, to_email, html_message=message)


def send_email_added_review(user):
    from_email = 'test@gmail.com'
    to_email = [user]

    message = render_to_string('added_review.html')

    send_mail("Вам оставили отзыв | You have received a review", message, from_email, to_email, html_message=message)


def send_email_to_support(data):
    account = settings.GMAIL_ACCOUNTS[1]
    host = account['EMAIL_HOST_USER']
    password_email = account["EMAIL_HOST_PASSWORD"]
    to_email = ['support@bazaarorigin.com']

    message = render_to_string('send_review.html', context=data)

    send_mail("New message to support", message, host, to_email, auth_user=host,
              auth_password=password_email, html_message=message)


def send_email_after_deactivate_ann(user):
    account = settings.GMAIL_ACCOUNTS[1]
    host = account['EMAIL_HOST_USER']
    password_email = account["EMAIL_HOST_PASSWORD"]
    to_email = [user]

    message = render_to_string('after_deactivate_ann.html')

    send_mail("The publication period has expired", message, host, to_email, auth_user=host,
              auth_password=password_email, html_message=message)


def send_email_after_deactivate_event(user):
    account = settings.GMAIL_ACCOUNTS[1]
    host = account['EMAIL_HOST_USER']
    password_email = account["EMAIL_HOST_PASSWORD"]
    to_email = [user]

    message = render_to_string('after_deactivate_event.html')

    send_mail("The publication period has expired", message, host, to_email, auth_user=host,
              auth_password=password_email, html_message=message)


def send_to_moderator_complaint(announcement_id):
    account = settings.GMAIL_ACCOUNTS[1]
    host = account['EMAIL_HOST_USER']
    password_email = account["EMAIL_HOST_PASSWORD"]
    to_email = ["support@bazaarorigin.com"]

    message = render_to_string('send_to_moderator_complaint.html')

    send_mail("Поступила жалоба / A complaint has been received", message, host, to_email, auth_user=host,
              auth_password=password_email, html_message=message)
