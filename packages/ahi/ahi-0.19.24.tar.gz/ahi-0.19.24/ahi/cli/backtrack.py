
import xml.etree.ElementTree as ET
import http.cookies
import urllib.parse
import dataclasses
import base64
import copy
import json
import re

from .. import response
from . import scaffolding


class ReconstructedHTTPMessage(response.Response):
    _top_line: str

    def __init__(self, http, url):
        self.url = url
        reserialised = dict()
        headers_text, body = http.split(b'\r\n\r\n', 1)
        try:
            reserialised['text'] = body.decode()
        except UnicodeDecodeError:
            reserialised['binary'] = base64.b64encode(body).decode()

        header_lines = re.split(r'[\r\n]+', headers_text.decode())
        self._parse_top_line(header_lines.pop(0), reserialised)

        headers_dict = dict([re.split(r':\s*', line, 1) for line in header_lines])
        reserialised['headers'] = response.HeadersCollection(headers_dict, None)
        super().__init__(serialised_cached_response=json.dumps(reserialised), url=url)


class ReconstructedRequest(ReconstructedHTTPMessage):
    def _parse_top_line(self, top_line, reserialised):
        # POST /boards/job.php HTTP/2
        top_line_match = re.search(r'^(\w+)\s+.*\s+HTTP/[\.\d]+$', top_line)
        self.verb = top_line_match.group(1)


class ReconstructedResponse(ReconstructedHTTPMessage):
    def _parse_top_line(self, top_line, reserialised):
        # HTTP/2 200 OK
        top_line_match = re.search(r'^HTTP/[\.\d]+\s+(\d+)\s+(.*)$', top_line)
        status_code, reserialised['reason'] = top_line_match.groups()
        reserialised['status_code'] = int(status_code)


class RequestResponse:
    def __init__(self, http_request, http_response, previous_pair, url):
        self.request = ReconstructedRequest(http_request, url)
        self.response = ReconstructedResponse(http_response, url)
        self._previous_pair = previous_pair
        self.url = url

    @property
    def history(self):
        pair = self
        while pair._previous_pair:
            pair = pair._previous_pair
            yield pair

    
def parse_burp_items(burp_items_path):
    tree = ET.parse(burp_items_path)
    root = tree.getroot()
    history = []
    previous_pair = None
    for elem in root:
        url = elem.find('url').text
        http_request = base64.b64decode(elem.find('request').text)
        http_response = base64.b64decode(elem.find('response').text)
        pair = RequestResponse(http_request, http_response, previous_pair, url)
        history.append(pair)
        previous_pair = pair
    return history


def _cookies_from_header(header_value):
    cookie = http.cookies.SimpleCookie()
    cookie.load(header_value)
    for k, o in cookie.items():
        yield k, o.value


@dataclasses.dataclass
class VarSource:
    transformation_code: str
    import_lines: set


def _find_var_source(var, context, layers=0):
    #input(f'Looking for {var} in {context}')
    if var == context:
        return VarSource()
    if var in context:
        return VarSource(transformation_code='regex, or split or something')
    if var.upper() == var and var.lower() in context:
        return VarSource(transformation_code='regex, or split or something, then .upper()')
    if var.lower() == var and var.upper() in context:
        return VarSource(transformation_code='regex, or split or something, then .lower()')
    if layers < 3:
        base64_encoded_var = base64.b64encode(var.encode()).decode()
        next_layer_var_source = _find_var_source(base64_encoded_var, context, layers=layers+1)
        if next_layer_var_source:
            return VarSource(f'base64.b64decode(({next_layer_var_source}).encode())',
                    next_layer_var_source.import_lines | set(('import base64', )))
        try:
            base64_decoded_var = base64.b64decode(var.encode()).decode()
            next_layer_var_source = _find_var_source(base64_decoded_var, context, layers=layers+1)
            if next_layer_var_source:
                return VarSource(f'base64.b64encode(({next_layer_var_source}).encode())',
                        next_layer_var_source.import_lines | set(('import base64', )))
        except:
            pass


def _add_prerequisite_requests(pair, script, comment, save_response_vars=dict()):
    target_request = pair.request
    # TODO: Find out how we could've known the contents for our request headers (except cookies).
    rewritten_headers = dict()
    rewritten_cookie = http.cookies.SimpleCookie()
    for name, value in target_request.headers.items():
        if scaffolding.should_explicitly_set_header(name, value, target_request.url):
            if name.lower() not in (
                    'cookie',
                    'content-type',
                    'origin',
                    'sec-fetch-site',
                    'referer',
                    'upgrade-insecure-requests',
                    ):
                for historic_pair in pair.history:
                    # Search response headers.
                    # TODO: Also search response body.
                    for historic_response_header_name, historic_response_header_value in historic_pair.response.headers.items():
                        if not historic_response_header_name.lower() in (
                                'content-length',
                                'date',
                                'server',
                                'cache-control',
                                'access-control-allow-credentials',
                                'access-control-allow-headers',
                                'access-control-allow-methods',
                                'access-control-allow-origin',
                                'access-control-expose-headers',
                                'access-control-max-age',
                                'age',
                                'content-security-policy',
                                'content-security-policy-report-only',
                                'content-type',
                                'cross-origin-opener-policy-report-only',
                                'cross-origin-resource-policy',
                                'etag',
                                'expect-ct',
                                'expires',
                                'last-modified',
                                'nel',
                                'ot-baggage-auth0-request-id',
                                'ot-tracer-sampled',
                                'ot-tracer-spanid',
                                'ot-tracer-traceid',
                                'p3p',
                                'pragma',
                                'referrer-policy',
                                'report-to',
                                'served-by',
                                'set-cookie',
                                'strict-transport-security',
                                'vary',
                                'via',
                                'x-amz-cf-id',
                                'x-amz-cf-pop',
                                'x-amz-version-id',
                                'x-auth0-requestid',
                                'x-cache',
                                'x-confluence-request-time',
                                'x-content-typeoptions',
                                'x-envoy-upstream-service-time',
                                'x-frame-options',
                                'x-powered-by',
                                'x-ratelimit-limit',
                                'x-ratelimit-remaining',
                                'x-ratelimit-reset',
                                'x-xss-protection',
                                ):
                            # Search in part of historic values (Location: https://magic.url/go#ohbythewaythisisyoursecretvalue)
                            # TODO: Search for an encoded or decoded form of our value in part of historic values
                            var_source = _find_var_source(value, historic_response_header_value)
                            if var_source:
                                var = scaffolding.pythonise_var_name(name)
                                # TODO: Imports dictated by var_source.
                                raise NotImplementedError(f'{var} = {var_source}')
                                #rewritten_cookie[name] = scaffolding.VariableReference(var)
                                #save_response_vars = {var: f'cookies[{cookie_name!r}]'}
                rewritten_headers[name] = value

            # TODO: Find out where our cookies were set.
            if name.lower() == 'cookie':
                for cookie_name, cookie_value in _cookies_from_header(value):
                    source_found = False
                    for historic_pair in pair.history:
                        # Looping over headers because theoretically, multiple Set-Cookie headers could exist.
                        # TODO: Also find cookie values in response body (set by Javascript)?
                        for historic_header_name, historic_header_value in historic_pair.response.headers.items():
                            if historic_header_name.lower() == 'set-cookie':
                                for historic_cookie_name, historic_cookie_value in _cookies_from_header(historic_header_value):

                                    if historic_cookie_value == cookie_value:
                                        # Do the required request and let requests.Session handle the cookie.
                                        _add_prerequisite_requests(
                                                pair = historic_pair,
                                                script = script,
                                                comment = f'Get cookie "{cookie_name}".',
                                                )
                                        source_found = True
                                        break
                            if source_found:
                                break
                        if source_found:
                            break
                    if not source_found:
                        rewritten_cookie[cookie_name] = cookie_value

    # FIXME: Set this as requests lib cookies.
    reserialised_cookie = '; '.join([part.strip() for part in re.split(r'\s*[\n\r]+\s*', rewritten_cookie.output(header=''), flags=re.DOTALL)])
    rewritten_headers['Cookie'] = reserialised_cookie
    

    # TODO: Find out how we could've known our GET paramaters.
    # TODO: Find out how we could've known our URL segments.
    # TODO: Find out how we could've known the contents for our request body.

    request = scaffolding.ScriptedRequest(
            target_request.verb,
            target_request.url,
            rewritten_headers,
            target_request.text,
            data_is_binary = bool(target_request._binary),
            comment = comment,
            save_response_vars = save_response_vars,
            )
    script.requests.append(request)


def proxy_history_to_ahi_code(history):
    script = scaffolding.Script()

    target_pair = history[-1]
    target_request = target_pair.request

    _add_prerequisite_requests(target_pair, script, comment='Last request in Burp items export. (Assuming this is what we ultimately wanted.)')

    return str(script)


def get_object_selector(var_name, o, value):
    '''Assume that JSON was parsed and a Python object o came out. Find value, and return Python code that extracts value from o, using var_name as the name of o.'''
    if o == value:
        return var_name
    elif isinstance(o, (str, int, float)):
        return None
    elif isinstance(o, dict):
        for k, v in o.items():
            selector = f'''{var_name}.get({k!r})'''
            if v == value:
                return selector
            elif result := get_object_selector(selector, v, value):
                return result
    elif isinstance(o, list):
        for v, i in zip(o, range(len(o))):
            selector = f'''{var_name}[{i}]'''
            if v == value:
                return selector
            elif result := get_object_selector(selector, v, value):
                return result
    else:
        raise NotImplementedError(
                f'Not yet capable of searching through {var_name} of type {type(o).__name__}. This function is designed to search through parsed JSON objects...')

