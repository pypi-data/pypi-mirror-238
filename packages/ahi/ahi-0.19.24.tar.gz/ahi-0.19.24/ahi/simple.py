#!/usr/bin/env python

from datetime import timedelta, datetime
from logging import *
import os.path
import inspect
import socket
import base64
import json
import time
import sys
import re

import requests
import urllib3
import parsel
import redis

from .response import *
from . import common


getLogger('requests').setLevel(WARNING)
getLogger('urllib3').setLevel(WARNING)
urllib3.disable_warnings()
HISTORY_KEY_TTL = 60 * 60 * 24 * 60
MAX_CACHE_RESPONSE_SIZE = 1024 * 1024
GOOGLEBOT_USER_AGENT_STRING = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
COMMON_USER_AGENT_STRING = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36' # From www.useragents.me, 2023-10-30.
_meta_tag_url_rex = re.compile(r'(?i)(?<=url=)\S+')


def clear_cache(url_pattern):
    '''Clear all cached responses for URL's matching 'url_pattern'.

    Examples:
    clear_cache('*example.com*')            # Clear for whole domain
    clear_cache('https://example.com/*')    # Clear for HTTPS version of the site
    clear_cache('*foo=bar*')                # Clear when this GET parameter was set
    '''
    r = common.get_redis_connection()
    i = 0
    for key in r.scan_iter(f'ahi:cache:{url_pattern}'):
        i += 1
        r.delete(key)
    info(f'{i} cached responses deleted.')


class HTTPClient(common.WebClient):
    def __init__(self, cache_ttl=timedelta(seconds=0), force_wait_interval=timedelta(seconds=0), auto_adjust_for_rate_limiting=True, logging_level=DEBUG, proxy='', user_agent=common.NOT_USED, default_headers=dict(), verify=True, allow_redirects=False, timeout=None, health_alert_report_url=common.NOT_USED, health_alert_report_mute_seconds=common.NOT_USED, breakage_handler=None, auth=None, cert=None, cookies=None):
        '''
        cache_ttl:                          Number of seconds (or a datetime.timedelta); how long to keep response in cache.
        force_wait_interval:                Hit the target host no more then once every so many seconds (or a datetime.timedelta).
        auto_adjust_for_rate_limiting:      HTTP status code 429 (Too Many Requests) automatically doubles our force_wait_interval.
        logging_level:                      Level for the Python logging instance.
        proxy:                              IP and port of a proxy to tunnel through, like: 'socks5://127.0.0.1:9050'.
        user_agent:                         The literal User-Agent header value to use. Handy constants are available.
        default_headers:                    Headers (a dict-like object) to send with every request.
        verify:                             Verify target's certificate. *
        allow_redirects:                    Automatically follow redirects and use the final response as the result.
        breakage_handler:                   If given, this lambda expression will be called with a BreakageError object when an "expect" statement fails.
        auth:                               HTTP authentication to do. *
        cert:                               Client side x509 certificate file path(s). See https://docs.python-requests.org/en/master/user/advanced/#client-side-certificates
        cookies:                            Cookies to prefill the cookiejar with. See https://docs.python-requests.org/en/master/user/advanced/#session-objects

        Several options can be overwritten per request.
        * see https://docs.python-requests.org/en/latest/api/#lower-level-classes

        WARNING: We use Requests sessions by default. This also means that cookies get stored in a jar.
        '''
        super().__init__(force_wait_interval=force_wait_interval, logging_level=logging_level, health_alert_report_url=health_alert_report_url, health_alert_report_mute_seconds=health_alert_report_mute_seconds, breakage_handler=breakage_handler)
        if type(cache_ttl) == timedelta:
            self.cache_ttl_seconds = int(cache_ttl.total_seconds())
        else:
            self.cache_ttl_seconds = int(cache_ttl)
        self.default_headers = default_headers
        self.requests_session_kwargs = {'timeout': timeout, 'allow_redirects': allow_redirects}
        if user_agent == common.NOT_USED:
            user_agent = COMMON_USER_AGENT_STRING
        if user_agent:
            self.default_headers['User-Agent'] = user_agent
        # WARNING: We use Requests sessions by default. This also means that cookies get stored in a jar.
        self.requests_library_client = requests.session()
        self.requests_library_client.verify = verify
        # This actually doesn't work as intended (upstream bug?), but adding the option to self.requests_session_kwargs does.
        self.requests_library_client.allow_redirects = allow_redirects
        if proxy:
            self.requests_library_client.proxies = {
                   'http':  proxy,
                   'https': proxy}
        self.requests_library_client.cert = cert
        self.auto_adjust_for_rate_limiting = auto_adjust_for_rate_limiting
        self.auth = auth
        if cookies:
            for cookie in cookies:
                self.cookies.set_cookie(cookie)

    
    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)
    def head(self, *args, **kwargs):
        return self.request('HEAD', *args, **kwargs)
    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)
    def patch(self, *args, **kwargs):
        return self.request('PATCH', *args, **kwargs)
    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)
    def request(self, verb, *args, **kwargs):
        '''Most arguments and keyword arguments are passed to the Requests library functions.

        expect: A bool to indicate whether we expect a succesful response (response code 200).
        '''
        try:
            url = args[0]
        except IndexError:
            url = kwargs['url']
        if verb.upper() == 'GET':
            if self.cache_ttl_seconds and self.r:
                # Caching is enabled. Try to get response from cache.
                serialised_cached_response = self.r.get(f'ahi:cache:{url}')
                if serialised_cached_response:
                    self.logger.debug(f'Getting {url} from cache.')
                    return Response(serialised_cached_response=serialised_cached_response, url=url)
            response = self._really_request(verb, *args, **kwargs)

            if self.cache_ttl_seconds:
                if self.r:
                    response_size = len(response)
                    if response_size > MAX_CACHE_RESPONSE_SIZE:
                        self.logger.warning(f'Not caching huge {url} response ({response_size} bytes).')
                    else:
                        # Caching is enabled and response is not huge. Save response to cache.
                        self.logger.debug(f'Caching {url} for {self.cache_ttl_seconds} seconds.')
                        self.r.set(f'ahi:cache:{url}', response.serialise(), ex=self.cache_ttl_seconds)
                else:
                    self.logger.warning(f'Caching requested, but no Redis found. (Start a Redis instance or set cache_ttl=0.)')
        else:
            response = self._really_request(verb, *args, **kwargs)
        return response


    @property
    def cookies(self):
        return self.requests_library_client.cookies
    

    def _really_request(self, verb, *args, **kwargs):
        try:
            url = args[0]
        except IndexError:
            url = kwargs['url']
        expect = kwargs.pop('expect', None)
        self.logger.debug(f'Doing {verb} request for {url}.')
        self._sleep_for_holdoff(url)

        # Use keyword args from this function call
        requests_library_function_kwargs = dict()
        for k, v in kwargs.items():
            requests_library_function_kwargs[k] = v
        if self.auth:
            requests_library_function_kwargs['auth'] = self.auth
        # Remove headers from keyword arguments to the Request constructor. In that function, they get mangled. (Casing-Gets-Corrected)
        headers = requests_library_function_kwargs.get('headers', dict())
        if headers:
            del requests_library_function_kwargs['headers']
        # Add default headers from this HTTPClient
        for default_header_name, default_header_value in self.default_headers.items():
            if default_header_name not in headers.keys():
                headers[default_header_name] = default_header_value
        # Enable streaming responses
        stream = requests_library_function_kwargs.get('stream', True)
        if not stream:
            self.logger.debug('Streaming is disabled. This means that resp.iter_content() will return the whole body at once, not in chunks.')
        if 'stream' in requests_library_function_kwargs.keys():
            # While stream is a parameter of requests.get(), it belongs to requests.PreparedRequest().send(), not requests.Request.__init__()
            del requests_library_function_kwargs['stream']
        requests_request = requests.Request(verb, *args, **requests_library_function_kwargs)
        prepped_request = self.requests_library_client.prepare_request(requests_request)
        for header_name, header_value in headers.items():
            prepped_request.headers[header_name] = header_value
        # Prepare the request body. Make if easy to use JSON encoding support.
        request_body_text = requests_library_function_kwargs.get('data')
        if request_body_text and not 'Content-Type' in prepped_request.headers.keys() and common.parses_as_json(request_body_text):
            self.logger.debug('The HTTP request body is parsable as JSON. You might want to set a header like \'Content-Type\': \'application/json;charset=utf-8\', or just do {verb.lower()}(url, json={request_body_text}).')
        retry_request = True
        error_count = 0
        while retry_request:
            try:
                if self.logger.isEnabledFor(DEBUG):
                    body_string = ''
                    if prepped_request.body:
                        body_string = f'\n\n{prepped_request.body}'
                    # FIXME: See how we should get the real TCP body from the prepped_request.
                    #        https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application#16630836
                    request_string = f'{prepped_request.method} {prepped_request.path_url} HTTP/something\n{HeadersCollection(prepped_request.headers, self)}{body_string}\n'
                    self.logger.debug(request_string)
                requests_library_response = self.requests_library_client.send(prepped_request, stream=stream, **self.requests_session_kwargs)
                # Patch! By default, the requests library seems to ignore the allow_redirects setting on session objects.
                # Actually, we seem to be able to work around this bug by adding the option to self.requests_session_kwargs.
                if not self.requests_library_client.allow_redirects and requests_library_response.history:
                    self.logger.warning(f'Followed redirects, despite setting allow_redirects = False. Using the oldest request in the chain.')
                    requests_library_response = requests_library_response.history[0]
                # Check for rate limiting
                if self.auto_adjust_for_rate_limiting and requests_library_response.status_code == 429:
                    # 429: 'Too Many Requests'
                    # Double our holdoff time.
                    self.force_wait_interval_seconds *= 2
                    instant_punishment_delay = self.force_wait_interval_seconds * 2
                    self.logger.warning(f'Got status code {requests_library_response.status_code}. Adjusting holdoff time to {self.force_wait_interval_seconds} seconds. Retrying this request in {instant_punishment_delay} seconds.')
                    retry_request = True
                    time.sleep(instant_punishment_delay)
                retry_request = False
            except requests.exceptions.ConnectionError as ex:
                if 'Temporary failure in name resolution' in str(ex) and error_count < 1:
                    error_count += 1
                    # After switching to a different network, above error handling did not suffice.
                    # From https://stackoverflow.com/questions/21356781/urrlib2-urlopen-name-or-service-not-known-persists-when-starting-script-witho :
                    # The behaviour you describe is, on Linux, a peculiarity of glibc. It only reads "/etc/resolv.conf" once, when loading. glibc can be forced to re-read "/etc/resolv.conf" via the res_init() function.
                    try:
                        import ctypes
                        libc = ctypes.cdll.LoadLibrary('libc.so.6')
                        res_init = libc.__res_init
                        res_init()
                    except:
                        raise ex
                else:
                    raise ex
        response = Response(requests_library_response=requests_library_response, url=url, ahi_client=self)
        if expect == False:
            # No expectations.
            pass
        elif expect == True:
            self.expect(response.ok, f'{verb} {url} failed with status {response.status_code} {response.reason}', response=response)
        elif type(expect) == int:
            self.expect(response.status_code == expect, f'{verb} {url} had status {response.status_code} {response.reason} instead of the expected {expect}', response=response)
        elif expect == None and response.ok:
            self.logger.debug(f'{verb} {url} was {response.status_code} {response.reason}. Get automatically alerted when this changes by using {verb.lower()}(url, expect=True) on {common.source_line().location}')
        return response

