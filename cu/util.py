import urllib
from flask import request, url_for


def is_safe_url(target):
    ref_url = urllib.parse(request.host_url)
    test_url = urllib.parse(urllib.join(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
