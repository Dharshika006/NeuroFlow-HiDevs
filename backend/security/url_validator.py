import re
import ipaddress
from urllib.parse import urlparse


URL_REGEX = r"^https?://"


def validate_url(
    url: str
):

    if not re.match(
        URL_REGEX,
        url
    ):
        return False

    try:

        parsed = urlparse(url)

        host = parsed.hostname

        if not host:
            return False

        if host in [

            "localhost",

            "127.0.0.1"

        ]:

            return False

        ip = ipaddress.ip_address(
            host
        )

        if (
            ip.is_private
            or
            ip.is_loopback
        ):
            return False

    except ValueError:
        pass

    return True