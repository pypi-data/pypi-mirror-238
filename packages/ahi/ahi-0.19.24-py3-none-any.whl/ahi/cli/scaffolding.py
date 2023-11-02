
import urllib.parse
import dataclasses
from pathlib import Path
import pprint
import json
import re

from .. import response
from .. import common


class VariableReference(str):
    def __repr__(self):
        return self


def pythonise_var_name(heathenscript):
    underscore_separated = re.sub(r'([a-z])([A-Z])', r'\1_\2', heathenscript)
    only_word_chars = re.sub(r'[^a-zA-Z]+', '_', underscore_separated)
    return only_word_chars.lower().strip('_')


def should_explicitly_set_header(name, value, url_or_domain):
    if '/' in url_or_domain:
        url_or_domain = urllib.parse.urlparse(url_or_domain).netloc.split(':')[0]
    if name == 'Host' and value == url_or_domain:
        # Don't explicitly set Host header if it's the same as the host from the URL.
        return False
    if name == 'Connection' and value == 'close':
        # Let Requests choose the TCP connection setting.
        return False
    if name in ('Content-Length',):
        # Let Requests calculate the content length after it has serialised the request body.
        return False
    if name == 'Accept' and value == '*/*':
        return False
    return True


def commandline_args_to_ahi_code(args):
    '''Convert curl compatible command line arguments to Python code using ahi.
    '''

    data = args.data or args.data_raw or args.data_binary

    http_method = 'get'
    if args.request:
        http_method = args.request.lower()
    elif data:
        http_method = 'post'

    script = Script()
    script.set_option('verify', args.insecure)
    script.set_option('allow_redirects', args.location)
    script.set_option('logging_level', args.verbose and 'DEBUG' or 'WARNING', repr_value=False)

    url_domain = urllib.parse.urlparse(args.url).netloc.split(':')[0]

    for header_line in args.header or []:
        name, value = header_line.split(': ', 1)
        if should_explicitly_set_header(name, value, url_domain):
            script.default_headers[name] = value

    if args.user:
        script.set_option('auth', tuple(args.user.split(':', 1)))

    cookie = args.cookie
    if cookie:
        cookie_creations = []
        for key_value in re.split(r';\s*', cookie):
            cookie_name, cookie_value = re.split(r'\s*=\s*', key_value, maxsplit=1)
            script.import_lines.add('import requests')
            cookie_creations.append(f'''requests.cookies.create_cookie(domain='{url_domain}',\n            name='{cookie_name}', value='{cookie_value}')''')
        script.set_option('cookies', '[' + ',\n        '.join(list(set(cookie_creations))) + ']', repr_value=False)

    if args.proxy:
        script.set_option('proxy', args.proxy)
        if args.proxy != 'http://127.0.0.1:8080':
            script.set_option('proxy', args.proxy, comment=repr('http://127.0.0.1:8080'))
    else:
        script.set_option('proxy', 'http://127.0.0.1:8080', commented_out=True)

    scripted_request = ScriptedRequest(
            verb = http_method,
            url = args.url,
            headers = dict(),
            data = data,
            data_is_binary = bool(args.data_raw or args.data_binary),
            comment = None,
            save_response_vars = dict(),
            )
    script.requests.append(scripted_request)
    if args.strip:
        # Script sets resp.
        exec('x = 42', globals(), locals())
        input(x)
        input(script)
        exec(str(script), globals(), locals())

        input(f'{resp=}')
        baseline_resp = resp
        input(f'{baseline_resp=}')
        for header_name, header_value in script.default_headers.items():
            # Remove a header, do the request, see if it gives a different response than the baseline.
            del script.default_headers[header_name]
            try:
                exec(str(script).replace('DEBUG', 'ERROR'), globals(), locals())
            except common.BreakageError:
                print(f'Stripping {header_name} header breaks something.')
                resp = None
            # Script sets resp.
            if resp != baseline_resp:
                # We broke something. Add header again.
                script.default_headers[header_name] = header_value
            else:
                if header_name == 'Newmanagementportal':
                    print(baseline_resp)
                    print('=')
                    print(resp)
                print(f'Stripping header {header_name}: {header_value}')
    return str(script)


@dataclasses.dataclass
class ScriptedRequest:
    verb: str
    url: str
    headers: response.HeadersCollection
    data: None
    data_is_binary: bool
    comment: str
    save_response_vars: dict
    files: dict = dataclasses.field(default_factory=dict)
    import_lines: set = dataclasses.field(default_factory=set)


    def __str__(self):
        self.verb = self.verb.lower()
        if self.verb in ('get', 'post', 'patch', 'put'):
            http_method_text = f'{self.verb}('
        else:
            http_method_text = f'request({self.verb.upper()!r}, '

        request_headers_param_text = ''
        request_headers_dict_text = ''
        if self.files:
            # post(url, files=files) only works automagically if we do not manually set the Content-Type to multipart/form-data (or anything else).
            self.headers.pop('Content-Type', None)
        if self.headers:
            request_headers_dict_text = 'headers = {'
            for k, v in self.headers.items():
                request_headers_dict_text += f'\n        {k!r}: {v!r},'
            request_headers_dict_text += '\n        }\n'
            request_headers_param_text = ', headers=headers'

        request_data_param_text = ''
        data_text = ''
        if self.data:
            request_data_param_text = f', data=request_data'
            data = self.data
            if isinstance(self.data, str):
                data = re.sub(r'\\"', '"', data)
                data = re.sub(r"'", r"\\'", data)
            if isinstance(data, dict):
                form_lines = []
                for k, v in data.items():
                    form_lines.append(f"'{k}': {repr(v)},")
                form_lines = '\n        '.join(form_lines)
                data_text = f"request_data = {{\n        {form_lines}\n        }}\n"
            elif not self.data_is_binary:
                if isinstance(self.data, str):
                    if '=' in data:
                        # data looks x-www-form-urlencoded
                        form_lines = []
                        unique_params = set()
                        all_params_are_unique = True
                        for kv in data.split('&'):
                            k, v = map(urllib.parse.unquote, kv.split('=', 1))
                            if k in unique_params:
                                all_params_are_unique = False
                                break
                            unique_params.add(k)
                            form_lines.append(f"'{k}': {repr(v)},")
                        if all_params_are_unique:
                            # Requests will assume that only one parameter with a certain name can exist.
                            form_lines = '\n        '.join(form_lines)
                            data_text = f"request_data = {{\n        {form_lines}\n        }}\n"
                    if not data_text and common.parses_as_json(self.data):
                        # Data parses as JSON. Use the json parameter instead of manually adding conversion and header.
                        pretty_json = pprint.pformat(json.loads(data), sort_dicts=False)
                        pretty_json = re.sub(r'^\{', '{\n ', pretty_json)
                        pretty_json = re.sub(r'^ ', '        ', pretty_json, flags=re.MULTILINE)
                        data_text = f'request_data = {pretty_json}\n'
                        request_data_param_text = f', json=request_data'
                else:
                    # data is not a string.
                    pretty_json = pprint.pformat(data)
                    pretty_json = re.sub(r'^\{', '{\n ', pretty_json)
                    pretty_json = re.sub(r'^ ', '        ', pretty_json, flags=re.MULTILINE)
                    data_text = f'request_data = json.dumps({pretty_json})\n'
                    self.import_lines.add('import json')
            if not data_text:
                # No fancy interpretation of data was possible. Just pass the raw data.
                data_text = f'# Use --data instead of --data-binary to try and deserialise this into a more usable Python data structure.\nrequest_data = {data!r}\n'
        request_files_text = ''
        request_files_param_text = ''
        if self.files:
            request_files_param_text = ', files=request_files'
            request_files_lines = []
            for form_field_name, file_info in self.files.items():
                match file_info:
                    case str(local_file_path):
                        request_files_lines.append(f"{form_field_name!r}: ({str(Path(local_file_path).name)!r}, open({local_file_path!r}, 'rb'))")
                    case _:
                        request_files_lines.append(f"{form_field_name!r}: ('{form_field_name}.txt', {file_info!r})")
            request_files_lines = '\n        '.join(request_files_lines)
            request_files_text = f'request_files = {{\n        {request_files_lines}\n        }}\n'
        comment_text = ''
        if self.comment:
            if isinstance(self.comment, str):
                comment_text = self.comment
            elif isinstance(self.comment, (list, tuple)):
                comment_text = '\n'.join(self.comment)
            comment_text = '# ' + comment_text.replace('\n', '\n# ') + '\n'

        response_var_saving_text = ''
        for var_name, var_access_code in self.save_response_vars.items():
            response_var_saving_text += f'{var_name} = {var_access_code}\n'
        return f'''{comment_text}{request_headers_dict_text}{data_text}{request_files_text}resp = c.{http_method_text}{self.url!r}{request_headers_param_text}{request_data_param_text}{request_files_param_text}, expect=True)
print(resp)
{response_var_saving_text}
'''


class Script:
    def __init__(self):
        self.import_lines = set([
            'import ahi',
            'from logging import *',
            ])
        self.default_headers = response.HeadersCollection(dict(), None)
        self._option_lines = dict()
        self.requests = list()
        self.variables = dict()
        self.missing_variables = set()

        self.set_option('cache_ttl', 0)
        self.set_option('force_wait_interval', 1)
        self.set_option('logging_level', 'DEBUG', repr_value=False)
        self.set_option('auto_adjust_for_rate_limiting', True)
        self.set_option('user_agent', "ahi.COMMON_USER_AGENT_STRING", repr_value=False)
        self.set_option('allow_redirects', False)
        self.set_option('breakage_handler', 'handle_breakage', repr_value=False, commented_out=True)
        self.set_option('auth', '(hardcoded.username, hardcoded.password)', commented_out=True, repr_value=False)
        self.set_option('cert', './client.pem', commented_out=True)
        self.set_option('cookies', None, commented_out=True)

    def set_option(self, name, value, commented_out=False, comment='', repr_value=True):
        if repr_value:
            s = f'{name} = {value!r},'
        else:
            s = f'{name} = {value},'
        if commented_out:
            s = f'#{s}'
        if comment:
            s = f'{s} # {comment}'
        self._option_lines[name] = s


    def __str__(self):
        # Take headers that are sent with every request out of the request-specific headers.
        # Put them in the default_headers.
        if not (default_headers := self.default_headers):
            for first_request in self.requests:
                if isinstance(first_request, ScriptedRequest):
                    default_headers = dict(first_request.headers)
                    break
            else:
                raise RuntimeError(
                        f'No requests found: {self.requests}')
        if len(self.requests) > 1:
            for req in self.requests:
                headers_not_in_all_requests = set()
                for k, v in default_headers.items():
                    if req.headers.get(k) != v:
                        headers_not_in_all_requests.add(k)
                for k in headers_not_in_all_requests:
                    #print(f'Deleting {k} from script')
                    del default_headers[k]
        for req in self.requests:
            if isinstance(req, ScriptedRequest):
                for k in default_headers.keys():
                    if k in req.headers.keys():
                        del req.headers[k]
                        #print(f'Deleting {k} from req')
                self.import_lines |= req.import_lines
        self.default_headers = response.HeadersCollection(default_headers, None)

        if self.default_headers:
            headers_dict_text = 'headers = {'
            for k, v in self.default_headers.items():
                headers_dict_text += f'\n        {k!r}: {v!r},'
            headers_dict_text += '\n        }\n'
            self.set_option('default_headers', 'headers', repr_value=False, comment='May want to move this to the \'headers\' argument of c.get()')
        else:
            headers_dict_text = ''

        variables_text = ''
        if self.variables:
            variables_text += '\n\n' + '\n'.join([f'{k} = {v!r}' for k, v in sorted(self.variables.items())])
        if self.missing_variables:
            variables_text += '\n\n# Missing variables (wil be prompted for upon first use):\n'
            variables_text += '\n'.join([f"{k} = hardcoded.{k}" for k in sorted(self.missing_variables) if k not in self.variables.keys()])
            self.import_lines.add('''try:
    import hardcoded
except ImportError:
    class H:
        _x = {} 
        def __getattr__(self, name):
            if not name in self._x:
                self._x[name] = input(f'Please enter {name}: ')
            return self._x[name]
    hardcoded = H()''')

        import_text = '\n'.join(reversed(sorted(self.import_lines, key=lambda l: len(l))))

        options_lines = '\n        '.join(self._option_lines.values())

        request_text = '\n\n'.join([str(part) for part in self.requests])

        return f'''#!/usr/bin/env python3
{import_text}{variables_text}

def handle_breakage(breakage_error):
    reporting_client = ahi.HTTPClient(logging_level=ERROR)
    try:
        reporting_client.post('http://127.0.0.1:8765/errors', data=breakage_error.asdict())
    except:
        pass

{headers_dict_text}c = ahi.HTTPClient(
        {options_lines}
        )

{request_text}'''
