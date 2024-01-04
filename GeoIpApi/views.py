import ipaddress

from flask import jsonify, request, make_response

from . import api
from .model import IPV4, IPV6
from .utils import convert_IP2int

from GeoIpCore.extensions import ServerCache, db
from GeoIpConfig.http.code import HTTP_400_BAD_REQUEST, HTTP_200_OK

from flask_caching import CachedResponse


@api.get("/")
def index():
    return "K"


@api.get("/ipv4/<string:ipv4>/")
@ServerCache.cached(make_cache_key=lambda *args, **kwargs: str(request.url))
def process_ipv4(ipv4):
    more = (request.args.get("more", None))

    if (type(intIP := convert_IP2int(ipv4)) != int):
        return CachedResponse(
            # """
            # views wraped by @cached can return this (which inherits from flask.Response)
            # to override the cache TTL dynamically
            # """
            response=make_response(jsonify({"status": "failed", "message": intIP}), HTTP_400_BAD_REQUEST),
            timeout=((60 * 60) * 6)
        )

    ip_db = (db.session.execute(
        db.select(IPV4)
        .filter(IPV4.StartRange <= intIP)
        .filter(IPV4.EndRange >= intIP)
    ).scalar_one_or_none())

    if not ip_db:
        return CachedResponse(
            response=make_response(jsonify(
                {"status": "failed", "message": "sorry we dont have any information about this ip address."}),
                HTTP_200_OK),
            timeout=((60 * 60) * 6)
        )
    if not more:
        return jsonify({"status": "success", "data": ip_db.serialize(intIP, ipv4)}), HTTP_200_OK
    else:

    # some query in countries
    return CachedResponse(
        response=make_response(jsonify({"status": "success", "more": more, "data": ip_db.serialize(intIP, ipv4)}), HTTP_200_OK),
        timeout=(60*60)*24 # 24 hour cashing its heavy response
    )
