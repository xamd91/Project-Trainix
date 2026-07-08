import os
import resend
from flask import render_template

resend.api_key = os.getenv('RESEND_API_KEY')

def send_email(to, subject, template, context=None):

    if context is None:
        context = {}

    html = render_template(
        f"notifications/{template}.html",
        **context
    )

    return resend.Emails.send({
        "from": "Trainix <noreply@anitrack.xyz>",
        "to": to,
        "subject": subject,
        "html": html
    })