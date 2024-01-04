import os
from celery import shared_task

templates = {

}

ActiveMailContent = {

}

ResetMailContext = {

}


def ReadTemplateContent(path):
    """This function take a template name and return content of that html"""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return " "


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


def sendActivAccounteMail(context: dict, recipients: list, **kwargs):
    """
    This Function send Activate Account mail

        context: dict
        values:
            token: slug url for activate user Account
    """

    template = Template(
        ReadTemplateContent(templates["activeAccount"])
    ).render(**context,
             **ActiveMailContent,
             **{"ActivateLink": url_for(
                 "auth.active_account", token=context['token'],
                 language=request.current_language,  # send user's language to endpoint as well
                 _external=True)})

    send_email(
        subject=ActiveMailContent["Subject"],
        sender=(_l('فعال سازی حساب کاربری'), current_app.config.get("MAIL_DEFAULT_SENDER", ":)")),
        recipients=recipients,
        html_body=template,
        **kwargs
    )


def sendResetPasswordMail(context: dict, recipients: list, **kwargs):
    """
    This Function send Reset Password Mail to users

        context: dict
        values:
            token: slug url for reset user Account
    """

    template = Template(
        ReadTemplateContent(templates["ResetPassword"])
    ).render(**context,
             **ResetMailContext,
             **{"ActivateLink": url_for(
                 "auth.check_reset_password", token=context['token'],
                 language=request.current_language,  # send user's language to endpoint as well
                 _external=True)})

    send_email(
        subject=ResetMailContext["Subject"],
        sender=(_l('بازنشانی گذرواژه'), current_app.config.get("MAIL_DEFAULT_SENDER", ":)")),
        recipients=recipients,
        html_body=template,
        **kwargs
    )