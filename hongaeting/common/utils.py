from django.core.mail import EmailMessage


def send_email(title, html_content, to_email):
    mail = EmailMessage(title, html_content, to=to_email)
    mail.content_subtype = 'html'
    mail.send()
