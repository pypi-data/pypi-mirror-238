
import urllib.parse
import pprint
import json
import re

from . import scaffolding
from .. import response

def http_to_ahi_code(args):
    '''Convert plain HTTP to Python code using ahi.
    '''

    with open(args.http, 'r') as f:
        http_string = f.read()

    script = scaffolding.Script()
    script.set_option('verify', args.insecure)

    url = urllib.parse.urlparse(args.url and args.url.pop() or 'https:///')
    headers = response.HeadersCollection(dict(), None)
    data = None
    empty_line_read = False
    for line in re.split(r'[\r\n]+', http_string):
        if first_line_match := re.search(r'^(\w+)\s+(.*)\s+(HTTP/[\d\.]+)$', line):
            http_method = first_line_match.group(1)
            url = url._replace(path=first_line_match.group(2))
        elif header_match := re.search(r'^([^:]+):\s*(.*)$', line):
            header_name, header_value = header_match.groups()
            match header_name.casefold():
                case 'host':
                    if (not url.netloc) or url.netloc.casefold() == header_value.casefold():
                        url = url._replace(netloc=header_value)
                    else:
                        headers[header_name] = header_value
                case 'cookie':
                    cookie_creations = []
                    for key_value in re.split(r';\s*', header_value):
                        cookie_name, cookie_value = re.split(r'\s*=\s*', key_value, maxsplit=1)
                        script.import_lines.add('import requests')
                        # FIXME: Race condition where args.url wins from Host header if the Cookie header comes early.
                        cookie_creations.append(f'''requests.cookies.create_cookie(domain='{url.netloc}',\n            name='{cookie_name}', value='{cookie_value}')''')
                    script.set_option('cookies', '[' + ',\n        '.join(list(set(cookie_creations))) + ']', repr_value=False)
                case _:
                    headers[header_name] = header_value
        elif line == '' and not empty_line_read:
            empty_line_read = True
        else:
            # Not a first line, not a header, not a neck. Must be a body.
            if not data:
                data = line
            else:
                data += '\n' + line
    # TODO: Maybe pass headers through scaffolding.should_explicitly_set_header(name, value, url_or_domain).

    scripted_request = scaffolding.ScriptedRequest(
        verb = http_method,
        url = urllib.parse.urlunparse(url),
        headers = headers,
        data = data,
        data_is_binary = bool(args.data_raw or args.data_binary),
        comment = args.http,
        save_response_vars = dict(),
        )
    script.requests.append(scripted_request)

    # TODO:
    #if args.user:
    #    script.set_option('auth', tuple(args.user.split(':', 1)))

    if args.proxy:
        script.set_option('proxy', args.proxy)
        if args.proxy != 'http://127.0.0.1:8080':
            script.set_option('proxy', args.proxy, comment=repr('http://127.0.0.1:8080'))
    else:
        script.set_option('proxy', 'http://127.0.0.1:8080', commented_out=True)

    return str(script)

