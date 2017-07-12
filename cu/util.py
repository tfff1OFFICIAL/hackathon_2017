import urllib.parse
from flask import request, url_for


def is_safe_url(target):
    ref_url = urllib.parse.urlparse(request.host_url)
    test_url = urllib.parse.urlparse(urllib.parse.urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def urlify_string(x):
    """
    Sanitise x to be able to form part of a URL
    :param x: String
    :return: String
    """
    return urllib.parse.quote(
        x.replace(" ", "-")
    )
