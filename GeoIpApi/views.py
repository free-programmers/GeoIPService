from GeoIpApi import api
from GeoIpCore.extensions import cache
from GeoIpApi.utils import search_in_ipv4, JsonAnswer, search_in_ipv6
from GeoIpCore.extensions import limiter


@api.route("/ipv4/<string:octetIP>/", methods=["GET"])
@limiter.limit("60 per minute")
@cache.cached(timeout=43200)
def process_ip_v4(octetIP):
    print("Answer Queried in db 11")
    return search_in_ipv4(octetIP)


@api.route("/ipv4/<string:octetIP>/<string:extra>/", methods=["GET"])
@limiter.limit("60 per minute")
@cache.cached(timeout=43200)
def process_ip_v4_extera(octetIP, extra):
    print("Answer Queried in db 21")
    if extra.lower() != "true":
        return JsonAnswer({"message": "Invalid Params", "status": "false", "x-Response-By": "https://ip2geo.ip"},
                          http_status=400)
    return search_in_ipv4(octetIP, True)


@api.route("/ipv6/<string:octetIP>/", methods=["GET"])
@limiter.limit("60 per minute")
@cache.cached(timeout=43200)
def process_ip_v6(octetIP):
    print("Answer Queried in db")
    return search_in_ipv6(octetIP)


@api.route("/ipv6/<string:octetIP>/<string:extra>/", methods=["GET"])
@limiter.limit("60 per minute")
@cache.cached(timeout=43200)
def process_ip_v6_extera(octetIP, extra):
    print("Answer Queried in db")
    if extra.lower() != "true":
        return JsonAnswer({"message": "Invalid Params", "status": "false", "x-Response-By": "https://ip2geo.ip"},
                          http_status=400)
    return search_in_ipv6(octetIP, True)
