from django.core.mail import send_mail as _send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_mail(
    target,
    template,
    subject="",
    source="noreply@lk.mai.ru",
    **kwargs,
):
    html = render_to_string(
        template + ".html",
        kwargs,
    )
    text = render_to_string(
        template + ".txt",
        kwargs,
    )
    if not isinstance(target, list):
        target = [target]
    _send_mail(
        subject,
        text,
        source,
        target,
        html_message=html,
    )
