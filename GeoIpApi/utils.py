import ipaddress
import json



def convert_IP2int(ip:str):
    try:
        ip = ipaddress.ip_address(ip)
    except Exception as e:
        return "invalid ip address"

    match ip:
        case ip.is_private:
            return "private ip address"
        case ip.is_loopback:
            return "loopback ip address"
        case ip.is_reserved:
            return "reserved ip address"

    return int(ip)


class IPserializer:
    def serialize(self):
        return {
        }



class IPV4serializer(IPserializer):
    ...



class IPV6serializer(IPserializer):
    ...