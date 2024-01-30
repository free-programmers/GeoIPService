# build in 
import pickle
from threading import Thread

from celery import shared_task
# framework
from flask import current_app, render_template
# libs
from flask_babel import lazy_gettext as _l
from flask_mail import Message

# app
from GeoIpCore.extensions import ServerMail


def async_send_email_thread(app, msg):
    """ Sending email asynchronously using threading lib """
    with app.app_context():
        ServerMail.send(msg)


@shared_task(ignore_result=True)
def async_send_email_celery(msg):
    """ Sending email asynchronously using celery """
    msg = pickle.loads(msg)
    ServerMail.send(msg)


def send_email(recipients: [], subject: str, sender: str, text_body: str = "", html_body: str = "",
               attachments: bool = None, async_thread: bool = False,
               async_celery: bool = False, language: str = "en"):
    """ This function sends mail via flask-mail
    Args:
        recipients:list = recipient of email (user's email address)
        subject:str = subject of email to send
        sender:str = sender email address
        text_body:str = email body
        html_body:str = if you want to send HTML email to can pass raw HTML
        attachments:blob = attachment files to be attached in email
        async_thread:bool = send email asynchronously using threading
        async_celery: bool = send email asynchronously using celery

        
        without this parameter, this function sends emails in sync mode
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
    """ This Function sends Activate Account mail

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
