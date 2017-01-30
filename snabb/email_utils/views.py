from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


def send_mail_template(user, template, substitutions):
    """This function sends email via sendgrid."""

    mail = EmailMultiAlternatives(
      subject=" ",
      body=" ",
      from_email="Snabb Team <no-reply@snabb.io>",
      to=[user.email, ],
      reply_to=["no-reply@snabb.io"]
    )
    # Add template
    mail.template_id = template
    # Replace substitutions in sendgrid template
    mail.substitutions = substitutions
    # Required for sendgrid.
    # If this not exists, send only plain text email.
    mail.attach_alternative(
        " ", "text/html"
    )
    mail.send()
