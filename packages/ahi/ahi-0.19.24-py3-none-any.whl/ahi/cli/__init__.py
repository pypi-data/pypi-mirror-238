
import argparse
import shlex
import sys
import re

from . import scaffolding
from . import postman
from . import openapi
from . import backtrack
from . import http

# These are needed when exec()ing our generated code. (Imports in exec()ed code don't work?)
from ..simple import HTTPClient
import ahi

class _DummyFlag():
    def __init__(self, *flags):
        self.flags = flags
        self.names = [f.strip('-') for f in flags]

    def name_matches(self, name):
        return name in self.names

    def add_to_parser(self, parser):
        parser.add_argument(*self.flags, action='store_true', help=argparse.SUPPRESS)


def _get_curl_command_from_stdin():
    print('Curl command line: ')
    input_text = sys.stdin.read()

    input_text = re.sub(r'(?<=\s)\$(?=\')', '', input_text)
    input_text = re.sub(r'\\\n', '', input_text)
    print(f'Input text:\n{input_text}\n')
    shlexer = shlex.shlex(input_text, posix=True)
    shlexer.whitespace_split = True
    #shlexer.escapedquotes = '"\''
    curl_cmd = list(shlexer)
    curl_cmd = shlex.split(input_text)
    if curl_cmd[0] == 'curl':
        curl_cmd = curl_cmd[1:]
    return curl_cmd


def command_line_entrypoint():
    parser = argparse.ArgumentParser()
    # Dummy options.
    dummy_flags = (
            _DummyFlag('-i', '--include'), # Include headers in output
            _DummyFlag('-s', '--silent'),
            )
    for d in dummy_flags:
        d.add_to_parser(parser)
    parser.add_argument('--strip', action='store_true', help='Strip headers as long as the response stays the same as the original one.')

    parser.add_argument('--postman', action='store', metavar='FILE', help='Convert Postman collection JSON file to Python code: %(prog)s --portman collection.json')
    parser.add_argument('--openapi', '--swagger', action='store', metavar='FILE', help='Convert OpenAPI JSON file to Python code: %(prog)s --openapi swagger.json')
    parser.add_argument('--burp-items', action='store', metavar='FILE', help='Use a Burp items export to build the minimal workflow up to the last request in the export: %(prog)s --burp-items exported.xml')
    parser.add_argument('--curl', action='store_true', help='Convert curl command to Python code: %(prog)s --curl https://example.com/')
    parser.add_argument('--http', action='store', metavar='FILE', help='Convert a plain HTTP request file to Python code: %(prog)s --http request.txt')
    # Curl compatible options we care about.
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable debug logging.')
    parser.add_argument('-x', '--proxy', action='store', help='Use the specified proxy.', metavar='protocol://host:port')
    parser.add_argument('-k', '--insecure', action='store_true', help='Proceed and operate even for server connections otherwise considered insecure.')
    parser.add_argument('-L', '--location', action='store_true', help='Allow redirects.')
    parser.add_argument('-X', '--request', action='store', help='Request method.')
    parser.add_argument('-H', '--header', action='append', help='Extra header.')
    parser.add_argument('-b', '--cookie', action='store', help='Cookie.')
    parser.add_argument('-u', '--user', action='store', help='Colon separated username and password for HTTP Authorization.')
    parser.add_argument('-d', '--data', action='store', help='Sends the specified data in a POST request to the HTTP server')
    parser.add_argument('--data-raw', action='store', help='This posts data similarly to -d, --data but without the special interpretation of the @ character.')
    parser.add_argument('--data-binary', action='store', help='This posts data exactly as specified with no extra processing whatsoever.')
    parser.add_argument('url', action='store', nargs='*', help='URL')
    if sys.argv == ['--curl',] or sys.argv == []:
        # Only --curl given, or no arguments at all. Get curl command line from stdin.
        args = parser.parse_args(_get_curl_command_from_stdin() + ['--curl',])
    else:
        args = parser.parse_args()

    # Use the first command line argument as a URL. (Shortcoming of argparse. Cannot mark an argument as optional.)
    args.url = args.url and args.url.pop()
    
    if args.postman:
        code = postman.postman_collection_to_ahi_code(args)
        print(code)
        return

    if args.openapi:
        code = openapi.openapi_to_ahi_code(args)
        print(code)
        return
    
    if args.http:
        code = http.http_to_ahi_code(args)
        print(code)
        return

    # Fix URL (naievely).
    if args.url and not re.search(r'^https?://', args.url):
        args.url = f'https://{args.url}'
    
    if args.burp_items:
        history = backtrack.parse_burp_items(args.burp_items)
        code = backtrack.proxy_history_to_ahi_code(history)
        print(code)
        return

    code = scaffolding.commandline_args_to_ahi_code(args)
    if args.curl:
        print(code)
    else:
        # Do a request using the exact code that we've generated as scaffolding.
        #print(f'Code:\n{code}\n')
        exec(code)

