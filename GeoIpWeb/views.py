import ipaddress
from flask import render_template, send_from_directory, flash, redirect, request, jsonify

from GeoIpWeb import web
from GeoIpConfig import BASE_DIR
from GeoIpWeb.form import ContactUSForm
from GeoIpWeb.model import ContactUS as ContactUsModel
from GeoIpCore.extensions import captchaVersion2, db, limiter,\
    cache



@web.get("/webStatic/<path:path>")
def WebStatic(path):
    return send_from_directory(BASE_DIR.joinpath("GeoIpWeb/static"), path)

@web.get("/")
@cache.cached(3600*8)
def index_view():
    return render_template("web/index.html")


@web.get("/contact-us/")
def contactUS():
    form = ContactUSForm()
    return render_template("web/contactUS.html", form=form)


@web.post("/contact-us/")
def contactUSPost():
    """
    this view take a post request for sibmitting a contact us form
    """
    form = ContactUSForm()
    if not form.validate():
        flash("some data are missing!", "danger")
        return render_template("web/contactUS.html", form=form)
    if not captchaVersion2.is_verify():
        flash("Captcha is incorrect!", "danger")
        return render_template("web/contactUS.html", form=form)

    contact_us = ContactUsModel()
    contact_us.SetPubicKey()
    contact_us.Email = form.Email.data
    contact_us.Title = form.Title.data
    contact_us.Message = form.Message.data
    try:
        db.session.add(contact_us)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        flash('Error 46', 'danger')
        return render_template("web/contactUS.html", form=form)
    else:
        flash('Form Submitted successfully', 'success')
        return redirect(request.referrer)

@web.get("/ip/")
@limiter.limit("60 per minute")
def PublicIpAddress():
    ip = request.headers.get('X-Real-IP', "NULL")
    return jsonify({
        "IPv4":ip if ip else "NULL",
        "IPv6":"NULL",
        "X-status":"X-Real-IP False",
        "x-Response-By": "www.ip2geo.ir"
    })

@web.get("/doc/Public-IP-Address/")
@cache.cached(43200)
def doc_public_ip_address():
    return render_template("web/docs/PublicIP.html")

@web.get("/doc/IP-to-Location/")
@cache.cached(43200)
def doc_ip_to_location():
    return render_template("web/docs/IP2Location.html")

@web.get("/Privacy-Terms-of-Use/")
@cache.cached(43200)
def privacy_term_of_use():
    return render_template("web/privacy.html")