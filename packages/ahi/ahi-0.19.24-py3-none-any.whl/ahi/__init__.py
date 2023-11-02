'''Using the simple HTTPClient
===========================
from logging import *
c = ahi.HTTPClient(cache_ttl=60, force_wait_interval=1, auto_adjust_for_rate_limiting=True, logging_level=DEBUG, proxy='http://127.0.0.1:8080', verify=True, allow_redirects=False, timeout=None)
resp = c.get('http://example.com/')
print(resp)

Using the Selenium driver for Firefox
=====================================
from logging import *
from selenium.webdriver.common.keys import Keys
ff = ahi.SeleniumFirefox(headless=True, force_wait_interval=timedelta(seconds=0), logging_level=DEBUG)
ff.get('https://example.com/')
ff.html.css('#LoginForm_Password').send_keys('P4$$w0rd')
ff.html.css('#LoginForm_Password').send_keys(Keys.RETURN)
ff.execute_script(\'\'\'SetLocation('\\x2Fdocs\\x2FProMyPlanning.aspx?_Division_=549942',event, 0)\'\'\')
ff.html.css('#Reports_Reports_Reports_MyPlanning').click()
print(ff.html)

Converting from a curl command line
===================================
ahi.curl_command_to_ahi_code() # Will prompt for input.
You can do the same thing from the command line:
$ girl --curl https://example.com/
'''

from .simple import *
try:
    from .selenium_firefox import *
    from .selenium_chrome import *
except ModuleNotFoundError as missing:
    if missing.name != 'selenium':
        raise missing
from .cli import *
from .response import *


_default_client = HTTPClient()
def hackingConfig(*args, **kwargs):
    global _default_client
    _default_client = HTTPClient(*args, **kwargs)
def get(*args, **kwargs):
    return _default_client.request('GET', *args, **kwargs)
def head(*args, **kwargs):
    return _default_client.request('HEAD', *args, **kwargs)
def post(*args, **kwargs):
    return _default_client.request('POST', *args, **kwargs)
def patch(*args, **kwargs):
    return _default_client.request('PATCH', *args, **kwargs)
def put(*args, **kwargs):
    return _default_client.request('PUT', *args, **kwargs)
def request(verb, *args, **kwargs):
    return _default_client.request(verb, *args, **kwargs)


__all__ = [
        # From here:
        'hackingConfig',
        'get',
        'head',
        'post',
        'patch',
        'put',
        'request',
        # From simple:
        'COMMON_USER_AGENT_STRING',
        'GOOGLEBOT_USER_AGENT',
        'clear_cache',
        'HTTPClient',
        # From selenium_firefox:
        'SeleniumFirefox',
        'SeleniumDocument',
        # From selenium_chrome:
        'SeleniumChrome',
        # From cli:
        'command_line_entrypoint',
        # From response:
        'Response',
        'Document',
        'URLCollection',
        ]
