from GeoIpCore import app
from flask import jsonify, request
import GeoIpConfig

@app.get("/ip/")
def PublicIpAddress():
    """
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
    ip = request.headers.get('Ar-Real-Ip', "NULL")
    code = request.headers.get('Ar-Real-Country', "NULL")
    return jsonify({
        "IPv4": ip if ip else "NULL",
        "IPv6": "NULL",
        "Country-Code": code if code else "NULL",
        "X-Status": "True" if ip and code else "False",
        "X-Response-By": "www.ip2geo.ir/ip/"
    })


@app.context_processor
def content_template_processor():
    ctx = {
        "base_domain": GeoIpConfig.BASE_DOMAIN
    }
    return ctx