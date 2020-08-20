# -*- coding: utf-8 -*-
"""Implements a simple wrapper around urlopen."""
import logging
import browser_cookie3
from functools import lru_cache
from http.client import HTTPResponse
from typing import Dict
from typing import Iterable
from typing import Optional
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import HTTPCookieProcessor
from urllib.request import build_opener

logger = logging.getLogger(__name__)


def _execute_request(
    url: str, method: Optional[str] = None, headers: Optional[Dict[str, str]] = None,
) -> HTTPResponse:
    if not url.lower().startswith("http"):
        raise ValueError("Invalid URL")

    base_headers = {"User-Agent": "Mozilla/5.0"}
    if headers:
        base_headers.update(headers)

    request = Request(url, method=method)
    request.headers.update(base_headers)

    try:
        raise Exception("AS")
        result = urlopen(request)  # nosec
    except Exception as e:  # catch 429 error
        # attempt to use cookies

        # use cookies browser to skip `Too many request`
        try:
            cookies_jar = browser_cookie3.chrome(domain_name=".youtube.com")
        except:
            cookies_jar = browser_cookie3.firefox(domain_name=".youtube.com")

        if cookies_jar is not None:
            return build_opener(HTTPCookieProcessor(cookies_jar)).open(request)

    return result


def get(url, extra_headers=None) -> str:
    """Send an http GET request.

    :param str url:
        The URL to perform the GET request for.
    :param dict extra_headers:
        Extra headers to add to the request
    :rtype: str
    :returns:
        UTF-8 encoded string of response
    """
    if extra_headers is None:
        extra_headers = {}
    return _execute_request(url, headers=extra_headers).read().decode("utf-8")


def stream(
    url: str, chunk_size: int = 4096, range_size: int = 9437184
) -> Iterable[bytes]:
    """Read the response in chunks.
    :param str url: The URL to perform the GET request for.
    :param int chunk_size: The size in bytes of each chunk. Defaults to 4KB
    :param int range_size: The size in bytes of each range request. Defaults
    to 9MB
    :rtype: Iterable[bytes]
    """
    file_size: int = range_size  # fake filesize to start
    downloaded = 0
    while downloaded < file_size:
        stop_pos = min(downloaded + range_size, file_size) - 1
        range_header = f"bytes={downloaded}-{stop_pos}"
        response = _execute_request(url, method="GET", headers={"Range": range_header})
        if file_size == range_size:
            try:
                content_range = response.info()["Content-Range"]
                file_size = int(content_range.split("/")[1])
            except (KeyError, IndexError, ValueError) as e:
                logger.error(e)
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            downloaded += len(chunk)
            yield chunk
    return  # pylint: disable=R1711


@lru_cache(maxsize=None)
def filesize(url: str) -> int:
    """Fetch size in bytes of file at given URL

    :param str url: The URL to get the size of
    :returns: int: size in bytes of remote file
    """
    return int(head(url)["content-length"])


def head(url: str) -> Dict:
    """Fetch headers returned http GET request.

    :param str url:
        The URL to perform the GET request for.
    :rtype: dict
    :returns:
        dictionary of lowercase headers
    """
    response_headers = _execute_request(url, method="HEAD").info()
    return {k.lower(): v for k, v in response_headers.items()}
