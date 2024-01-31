import ipaddress


def is_public_ip_v6(ip: str):
    """This Function validate is an IP Address is valid or not
    Returns True if the IPv6 address is public, False otherwise.
    """
    try:
        ip = ipaddress.ip_address(ip)
        if ip.version != 6:
            raise ValueError
    except ValueError:
        return False

    return ip if not ip.is_link_local and not ip.is_loopback and not ip.is_reserved else False


def convert_IP2intv6(ip: str):
    """Converts an IPv6 address to an integer, handling various cases."""
    if not (ip := is_public_ip_v6(ip)):
        return "invalid ip address"

    return int(ip)


def is_public_ip_v4(ip: str):
    """Returns True if the IP address is public, False otherwise."""
    try:
        ip = ipaddress.ip_address(ip)
        if ip.version != 4:
            raise ValueError
    except ValueError:
        return False

    return ip if not ip.is_private and not ip.is_loopback and not ip.is_reserved else False


def convert_IP2intv4(ip: str):
    """Converts an IP address to an integer, handling various cases."""

    if not (ip := is_public_ip_v4(ip)):
        return "invalid ip address"

    return int(ip)

