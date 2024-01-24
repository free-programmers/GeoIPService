# framework
from flask import jsonify, request, make_response

# app
from . import api
from .model import IPV4, IPV6, CountryInfo
from .utils import convert_IP2intv6, convert_IP2intv4

from GeoIpCore.extensions import ServerCache, db, ServerRequestLimiter
from GeoIpConfig.http.code import HTTP_400_BAD_REQUEST, HTTP_200_OK
from GeoIpCore.utils import Make_API_Cache_Key

# libs
from flask_caching import CachedResponse


@api.get("/ipv4/<string:ipv4>/")
@ServerRequestLimiter.limit("60/minute")
@ServerCache.cached(make_cache_key=Make_API_Cache_Key)
def process_ipv4(ipv4):
    more = (request.args.get("more", None))

    if (type(intIP := convert_IP2intv4(ipv4)) != int):
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
            response=make_response(
                jsonify({"status": "failed", "message": "sorry we dont have any information about this ip address."}),
                HTTP_200_OK),
            timeout=((60 * 60) * 6)
        )

    if not more or more != '1':
        return jsonify({"status": "success", "data": ip_db.serialize(intIP, ipv4)}), HTTP_200_OK

    CountryFullInfo = db.session.execute(
        db.select(CountryInfo).filter_by(CountryCode=ip_db.CountryCode)).scalar_one_or_none()

    if not CountryFullInfo:
        return jsonify(
            {"more": "failed to fetch data", "status": "success", "data": ip_db.serialize(intIP, ipv4)}), HTTP_200_OK

    return jsonify(
        {"more": CountryFullInfo.serialize(), "status": "success", "data": ip_db.serialize(intIP, ipv4)}), HTTP_200_OK


@api.get("/ipv6/<string:ipv6>/")
@ServerRequestLimiter.limit("60/minute")
@ServerCache.cached(make_cache_key=Make_API_Cache_Key)
def process_ipv6(ipv6):
    more = (request.args.get("more", None))

    if (type(intIP := convert_IP2intv6(ipv6)) != int):
        return CachedResponse(
            # """
            # views wraped by @cached can return this (which inherits from flask.Response)
            # to override the cache TTL dynamically
            # """
            response=make_response(jsonify({"status": "failed", "message": intIP}), HTTP_400_BAD_REQUEST),
            timeout=((60 * 60) * 6)
        )

    ip_db = (db.session.execute(
        db.select(IPV6)
        .filter(IPV6.StartRange <= intIP)
        .filter(IPV6.EndRange >= intIP)
    ).scalar_one_or_none())

    if not ip_db:
        return CachedResponse(
            response=make_response(jsonify({"status": "failed", "message": "sorry we dont have any information about this ip address."}), HTTP_200_OK),
            timeout=((60 * 60) * 6)
        )
    if not more or more != '1':
        return jsonify({"status": "success", "data": ip_db.serialize(intIP, ipv6)}), HTTP_200_OK

    CountryFullInfo = db.session.execute(
        db.select(CountryInfo).filter_by(CountryCode=ip_db.CountryCode)).scalar_one_or_none()

    if not CountryFullInfo:
        return jsonify(
            {"more": "failed to fetch data", "status": "success", "data": ip_db.serialize(intIP, ipv6)}), HTTP_200_OK

    return jsonify(
        {"more": CountryFullInfo.serialize(), "status": "success", "data": ip_db.serialize(intIP, ipv6)}), HTTP_200_OK
