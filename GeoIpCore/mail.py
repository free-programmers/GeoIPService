import pickle

from flask import current_app, render_template
from flask_mail import Message
from flask_babel import lazy_gettext as _l
from threading import Thread

from GeoIpCore.extensions import ServerMail
from celery import shared_task


def async_send_email_thread(app, msg):
    """
    Sending email asynchronously using threading
    """
    with app.app_context():
        ServerMail.send(msg)


@shared_task(ignore_result=True)
def async_send_email_celery(msg):
    """
    Sending email asynchronously using celery
    """
    msg = pickle.loads(msg)
    ServerMail.send(msg)


def send_email(recipients, subject, sender, text_body="", html_body="",
               attachments=None, async_thread=False, async_celery=False, language: str = "en"):
    """
        this function send mail via flask-mail

        recipients = recipient of email (user's email address)
        subject = subject of email to send
        sender = sender email address
        text_body = email body
        html_body = if you want to send html email to can pass raw html
        attachments = attachment files to be attached in email
        async_thread : send email asynchronously using threading
        async_celery : send email asynchronously using celery
        without this parameter this function send email sync
    """

    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)

    if async_thread:
        current_app.logger.info(f"\n[Thread Async] Mail Sending {recipients}")
        Thread(target=async_send_email_thread, args=(current_app._get_current_object(), msg)).start()

    elif async_celery:
        current_app.logger.info(f"\n[Celery Async] Mail Sending {recipients}")
        async_send_email_celery.delay(pickle.dumps(msg))

    else:
        current_app.logger.info(f"\n[Sync Normal] Mail Sending {recipients}")
        ServerMail.send(msg)


def sendActivateAccountMail(context: dict = {}, recipients: list = [], **kwargs):
    """
    This Function send Activate Account mail

        context: dict
        values:
            token: slug url for activate user Account
    """

    template = render_template("mail/activate-account.html", **context)

    send_email(
        subject=_l("activate account"),
        sender=(_l('activate account'), current_app.config.get("MAIL_DEFAULT_SENDER", ":)")),
        recipients=recipients,
        html_body=template,
        **kwargs
    )
