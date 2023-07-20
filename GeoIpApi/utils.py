import json
import time
import ipaddress

from flask import jsonify
from GeoIpApi.model import CountryInfo, IPV4 as IPV4db, IPV6 as IPV6db
from GeoIpConfig import BASE_DOMAIN

def Convert2_IPv4(ip:str) -> ipaddress.IPv4Address:
    """
    this function take an ip and convert it to ipaddress.ipv4
    """
    try:
        ip = ipaddress.ip_address(ip)
    except ValueError:
        return False

    if not isinstance(ip, ipaddress.IPv4Address):
        return False

    return ip

def Convert2_IPv6(ip:str) -> ipaddress.IPv6Address:
    """
    this function take an ip and convert it to ipaddress.ipv4
    """
    try:
        ip = ipaddress.ip_address(ip)
    except ValueError:
        return False

    if not isinstance(ip, ipaddress.IPv6Address):
        return False

    return ip



def JsonAnswer(data:dict={},http_status=200 ):
    """Return a Json Answer"""
    return jsonify(data), http_status

class IPv6erializer:
    """
    This CLass Serialize IPV4 Data for sending back to user
    """
    __IPV6 = None
    __DATA = {}

    def __init__(self, IpV6Object: IPV6db):
        if not isinstance(IpV6Object, IPV6db):
            raise ValueError("input most be a ip table")

        self.__IPV6 = IpV6Object


    def serializer(self):
        """
        this method add base info about ip
        """
        data = {
            "Country": {
                "name":self.__IPV6.CountryName,
            },
            "CountryCode": self.__IPV6.CountryCode,
            "City": self.__IPV6.CityName,
            "State": self.__IPV6.StateName,
            "Latitude": self.__IPV6.Lat,
            "Longitude": self.__IPV6.Long,
            "ZipCode": self.__IPV6.ZipCode,
            "TimeZone": self.__IPV6.TimeZone,
            "IPv6": {
                "ip": self.__IPV6.octet_ip or "Null",
                "decimal": self.__IPV6.decimal_ip or "Null",
                "hex": self.__IPV6.hex_ip or "Null",
            },
            "x-Response-BY":f"{BASE_DOMAIN}/api/v1/ipv6/{self.__IPV6.octet_ip}"
        }
        self.__DATA.update(data)


    def Additionalserializer(self, CountryINFO):
        """
        this method add additional info about ip
        /true
        """
        if CountryINFO:
            data = json.loads(CountryINFO.Info)
            country = {
                "officialName":data["name"]["official"],
                "nativeName":data["name"]["nativeName"],
                "capital":data["capital"],
                "capitalInfo":data["capitalInfo"],
                "region":data["region"],
                "subregion":data["subregion"],
                "languages":data["languages"],
                "translations":data["translations"],
                "flag":data["flag"],
                "maps":data["maps"],
                "continents":data["continents"],
                "flags":data["flags"]
            }
            dt = {
                "tld":data["tld"],
            }

            self.__DATA["Country"].update(country)
            self.__DATA.update(dt)

    def getSerialize(self):
        return self.__DATA




class IPv4Serializer:
    """
    This CLass Serialize IPV4 Data for sending back to user
    """
    __IPV4 = None
    __DATA = {}

    def __init__(self, IpV4Object: IPV4db):
        if not isinstance(IpV4Object, IPV4db):
            raise ValueError("input most be a ip table")

        self.__IPV4 = IpV4Object


    def serializer(self):
        """
        this method add base info about ip
        """
        data = {
            "Country": {
                "name":self.__IPV4.CountryName,
            },
            "CountryCode": self.__IPV4.CountryCode,
            "City": self.__IPV4.CityName,
            "State": self.__IPV4.StateName,
            "Latitude": self.__IPV4.Lat,
            "Longitude": self.__IPV4.Long,
            "ZipCode": self.__IPV4.ZipCode,
            "TimeZone": self.__IPV4.TimeZone,
            "IPv4": {
                "octet": self.__IPV4.octet_ip or "Null",
                "decimal": self.__IPV4.decimal_ip or "Null",
                "hex": self.__IPV4.hex_ip or "Null",
            },
            "x-Response-BY":f"{BASE_DOMAIN}/api/v1/ipv4/{self.__IPV4.octet_ip}"
        }
        self.__DATA.update(data)


    def Additionalserializer(self, CountryINFO):
        """
        this method add additional info about ip
        /true
        """
        if CountryINFO:
            data = json.loads(CountryINFO.Info)
            country = {
                "officialName":data["name"]["official"],
                "nativeName":data["name"]["nativeName"],
                "capital":data["capital"],
                "capitalInfo":data["capitalInfo"],
                "region":data["region"],
                "subregion":data["subregion"],
                "languages":data["languages"],
                "translations":data["translations"],
                "flag":data["flag"],
                "maps":data["maps"],
                "continents":data["continents"],
                "flags":data["flags"]
            }
            dt = {
                "tld":data["tld"],
            }

            self.__DATA["Country"].update(country)
            self.__DATA.update(dt)

    def getSerialize(self):
        return self.__DATA




def search_in_ipv4(octetIP, extera=False):
    """

    """
    IPV4 = Convert2_IPv4(octetIP)
    if not IPV4:
        return JsonAnswer(
            data=
            {
                "message": "invalid IP address",
                "status": "False",
                "ip": octetIP,
                "time": (time.time())
            }, http_status=400)

    if IPV4.is_private:
        return JsonAnswer(
            data=
            {
                "message": "IP address is private",
                "status": "False",
                "ip": octetIP,
                "time": (time.time())
            },http_status=400)

    if IPV4.is_reserved:
        return JsonAnswer(
            data=
            {
                "message": "IP address is reserved",
                "status": "False",
                "ip": octetIP,
                "time": (time.time())
            },http_status=400)

    decimalIP = int(IPV4)
    ipLOOKup = IPV4db.query.filter(IPV4db.StartRange <= decimalIP).filter(IPV4db.EndRange >= decimalIP).first()

    if not ipLOOKup:
        return JsonAnswer(
            data=
            {
                "message": "Cant Find ip in db",
                "status": "False",
                "ip": octetIP,
                "time": str(time.time())
            },http_status=404)

    ipLOOKup.decimal_ip = decimalIP
    ipLOOKup.hex_ip = str(hex(decimalIP))
    ipLOOKup.octet_ip = octetIP

    serializer = IPv4Serializer(ipLOOKup)
    serializer.serializer()

    if extera:
        countryDB = CountryInfo.query.filter(CountryInfo.CountryCode == ipLOOKup.CountryCode).first()
        serializer.Additionalserializer(countryDB)

    return jsonify(serializer.getSerialize()), 200




def search_in_ipv6(octetIP, extera=False):
    """
        Search in IPV6 Tables for ip
    """
    IPV6 = Convert2_IPv6(octetIP)
    if not IPV6:
        return JsonAnswer(
            data=
            {
                "message": "invalid IP address",
                "status": "False",
                "ip": octetIP,
                "time": (time.time())
            }, http_status=400)


    decimalIP = int(IPV6)
    ipLOOKup = IPV6db.query.filter(IPV6db.StartRange <= decimalIP).filter(IPV6db.EndRange >= decimalIP).first()

    if not ipLOOKup:
        if IPV6.is_private:
            return JsonAnswer(
                data=
                {
                    "message": "IP address is private",
                    "status": "False",
                    "ip": octetIP,
                    "time": (time.time())
                }, http_status=400)
        if IPV6.is_reserved:
            return JsonAnswer(
                data=
                {
                    "message": "IP address is reserved",
                    "status": "False",
                    "ip": octetIP,
                    "time": (time.time())
                }, http_status=400)

        return JsonAnswer(
            data=
            {
                "message": "Cant Find ip in db",
                "status": "False",
                "ip": octetIP,
                "time": str(time.time())
            }, http_status=404)

    ipLOOKup.decimal_ip = decimalIP
    ipLOOKup.hex_ip = str(hex(decimalIP))
    ipLOOKup.octet_ip = octetIP

    serializer = IPv6erializer(ipLOOKup)
    serializer.serializer()

    if extera:
        countryDB = CountryInfo.query.filter(CountryInfo.CountryCode == ipLOOKup.CountryCode).first()
        serializer.Additionalserializer(countryDB)

    return jsonify(serializer.getSerialize()), 200