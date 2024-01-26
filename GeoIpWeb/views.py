import ipaddress


# app
from . import web
from . import form as WebForm, model as WebModel
from GeoIpCore.extensions import ServerCaptcha2

# framework
from flask import render_template, flash, redirect,  request, jsonify, url_for, get_flashed_messages


from flask_babel import lazy_gettext as _l





@web.route("/", methods=["GET"])
def index_get() -> str:
    """Render Index Page"""
    return render_template("web/index.html")


@web.route("/terms/", methods=["GET"])
def term_get() -> str:
    """Render term of use privacy page to user"""
    return render_template("web/term-of-use.html")


@web.route("/contact-us/", methods=["GET"])
def contact_us_get() -> str:
    """Render term of use privacy page to user"""
    form = WebForm.ContactUsForm()
    return render_template("web/contact-us.html", form=form)


@web.route("/contact-us/", methods=["POST"])
def contact_us_post() -> str:
    """saving contact us messages"""
    form = WebForm.ContactUsForm()
    if not ServerCaptcha2.is_verify():
        flash(_l("invalid captcha"), "daner")
        form.form_errors.append(_l("invalid captcha"))
        return render_template("web/contact-us.html", form=form)

    if not form.validate():
        flash(_l("invalid request"), "daner")
        form.form_errors.append(_l("invalid request"))
        return render_template("web/contact-us.html", form=form)

    contactUS = WebModel.ContactUS()
    contactUS.Title = form.Title.data
    contactUS.Message = form.Message.data
    contactUS.Email = form.Email.data
    contactUS.SetPublicKey()
    contactUS.save()
    flash(_l("Thanks for your message, we will contact you as soon as possible"), "success")
    return redirect(request.referrer)


@web.route("/about-us/", methods=["GET"])
def about_us_get() -> str:
    """Render about us page"""
    return render_template("web/about-us.html")



@web.route("/ip/", methods=["GET"])
def userOwnIP():
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
    # https://docs.arvancloud.ir/fa/cdn/headers/
    """
    this view return information about user ip address

    ArvanCloud http header sample
        - X-Real-Ip: 10.11.7.156
        - Host: www.ip2geo.ir
        - X-Forwarded-For: 164.215.236.103, 94.101.182.4, 10.11.7.156
        - X-Forwarded-Proto: https
        - X-Forwarded-Port: 80
        - X-Forwarded-Host: www.ip2geo.ir
        - Connection: close
        - User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0
        - Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
        - Accept-Encoding: gzip, deflate, br
        - Accept-Language: en-US,en;q=0.5
        - Ar-Real-Country: IR
        - Ar-Real-Ip: 164.215.236.103
        - Ar-Sid: 2062
        - Cdn-Loop: arvancloud; count=1
        - Sec-Fetch-Dest: document
        - Sec-Fetch-Mode: navigate
        - Sec-Fetch-Site: none
        - Sec-Fetch-User: ?1
        - True-Client-Ip: 164.215.236.103
        - Upgrade-Insecure-Requests: 1
        - X-Country-Code: IR
        - X-Forwarded-Server: server code
        - X-Request-Id: some random string
        - X-Sid: 2062
    """
    ip = request.headers.get('True-Client-Ip', request.headers.get("Ar-Real-Ip", None))
    Country_code_2D = request.headers.get('X-Real-Country', None)

    v4intIP = 0
    if ip and ip != "NULL":
        v4intIP = int(ipaddress.ip_address(ip))

    return jsonify({
        "ip": {
            "v4": {
                "hex": hex(v4intIP),
                "decimal": v4intIP,
                "octet": ip
            },
            "v6": {
                "hex": hex(0),
                "decimal": 0,
                "octet": None
            },
        },
        "Country-Code": Country_code_2D,
        "X-Status": True if ip and Country_code_2D else False,
        "more": {
            "v4": url_for('api.process_ipv4', ipv4=ip, _external=True) if ip else None,
            "v6": None
        },
    })


@web.get("/get/notifications/")
def get_notification():
    """Notification Messages view
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This view return user all flash messages in a json


    arguments:
        None -- clear

    return:
        return all flash messages in a json format
    """
    flashes = []
    messages = get_flashed_messages(with_categories=True)

    for category, message in messages:
        temp = {"message": message, "category": category}
        flashes.append(temp)
    return jsonify(flashes)


