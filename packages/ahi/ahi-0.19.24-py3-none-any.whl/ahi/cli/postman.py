
import urllib.parse
import secrets
import pprint
import json
import re

from . import scaffolding

def postman_collection_to_ahi_code(args):
    '''Convert Postman collection JSON to Python code using ahi.
    '''

    with open(args.postman, 'r') as f:
        postman_collection = json.load(f)

    script = scaffolding.Script()
    script.set_option('verify', args.insecure)

    def reference_variables(s, quote=True):
        if not isinstance(s, str):
            return s
        string_with_python_references = ''
        prev_match_end = 0
        variables_referenced = 0
        for postman_variable_reference in re.finditer(r'{{(.*?)}}', s):
            string_with_python_references += s[prev_match_end:postman_variable_reference.start()]
            var_name = scaffolding.pythonise_var_name(postman_variable_reference.group(1))
            if var_name not in script.variables.keys():
                script.missing_variables.add(var_name)
            string_with_python_references += '{' + var_name + '}'
            prev_match_end = postman_variable_reference.end()
            variables_referenced += 1
        string_with_python_references += s[prev_match_end:]
        if variables_referenced == 0:
            if quote:
                return repr(string_with_python_references)
            else:
                return string_with_python_references
        elif variables_referenced == 1 \
                and postman_variable_reference.start() == 0 \
                and postman_variable_reference.end() == len(s):
            if quote:
                # Only returning the raw variable name if we were supposed to be quoting every other string.
                return var_name
            else:
                #raise ValueError(f'Cannot refer to variable "{var_name}" if we\'re not allowed to define quotes around it.')
                return scaffolding.VariableReference(var_name)
        else:
            if quote:
                return 'f' + repr(string_with_python_references)
            else:
                return string_with_python_references
    
    url_domain = None
    if args.url:
        url_scheme = urllib.parse.urlparse(args.url).scheme
        url_netloc = urllib.parse.urlparse(args.url).netloc
        script.variables['host'] = f'{url_scheme}://{url_netloc}'
        url_domain = url_netloc.split(':')[0]

    stats = dict()
    total_endpoints = 0
    for postman_item in postman_collection.get('item', []):
        for header in postman_item.get('request', dict()).get('header', []):
            key_info = stats.get(header.get('key'), dict())
            key_info['count'] = key_info.get('count', 0) + 1
            existing_values = set(key_info.get('values', []))
            key_info['values'] = existing_values | set((reference_variables(header.get('value'), quote=False),))
            stats[header.get('key')] = key_info
            total_endpoints += 1

    def pythonize_variable_name(s):
        return re.sub(r'^[^a-z]+', '', re.sub(r'\W+', '_', s).lower()).strip('_')

    header_variables = dict()
    for header, header_info in stats.items():
        if len(header_info.get('values')) == 1:
            header_value = header_info.get('values').pop()
            if isinstance(header_value, str) and len(header_value) > len(header):
                header_variable_name = pythonize_variable_name(header)
                script.variables[header_variable_name] = header_value
                header_variables[header_value] = header_variable_name
            
    def parse_postman_item_list(postman_item_list):
        for postman_item in postman_item_list:
            comments = []
            if set(postman_item.keys()) == set(('name', 'item')):
                folder_description = postman_item.get('name')
                comments.append(folder_description)
                parse_postman_item_list(postman_item.get('item'))
                continue
            elif not set(('name', 'request', 'response')) <= set(postman_item.keys()):
                continue
            comments.append(postman_item.get('name'))
            if description := postman_item.get('description'):
                comments.append(description)
            
            postman_request = postman_item.get('request')
            if not postman_request:
                raise NotImplementedError(f'No request found in Postman item: {postman_item}')
            for unknown_field in set(postman_request.keys()) - set(('method', 'url', 'header', 'body', 'description', 'auth')):
                #print(f'# Warning: encountered unknown field "{unknown_field}" in Postman JSON.')
                raise NotImplementedError(f'# Warning: encountered unknown field "{unknown_field}" in Postman JSON. (With value: {postman_request.get(unknown_field)})')

            headers = dict()
            postman_body = postman_request.get('body')
            body_mode = postman_body and postman_body.get('mode')
            body = dict()
            files = dict()
            if (not postman_body) or postman_body == {'mode': 'raw', 'raw': ''}:
                pass
            elif body_mode == 'formdata':
                headers['Content-Type'] = 'multipart/form-data'
                if not (formdata := postman_body.get('formdata')):
                    raise KeyError(
                            f'No formdata key in {postman_item}')
                for formdata_key_value in formdata:
                    match formdata_key_value:
                        case {'key': form_field_name, 'type': 'file', 'src': str(local_file_path)}:
                            if form_field_name in files:
                                form_field_name = scaffolding.pythonise_var_name(local_file_path)
                                if form_field_name in files:
                                    form_field_name = secrets.token_urlsafe()
                            files[form_field_name] = local_file_path
                        #case {'key': str(k), 'value': str(v), 'type': 'text'}:
                        case {'key': str(k), 'value': v}:
                            body[k] = v
                        case _:
                            raise NotImplementedError(
                                    f'Unexpected formdata item: {formdata_key_value}')
                #_ = [repr(formdata_key_value) for formdata_key_value in postman_body['formdata']]
            elif body_mode not in ('raw',):
                #print(f'# Warning: encountered unknown HTTP request body mode "{body_mode}" in Postman JSON.')
                raise NotImplementedError(
                        f'# Warning: encountered unknown HTTP request body mode "{body_mode}" in Postman JSON: {postman_body}.')
            elif data := postman_body.get('raw'):
                data_is_json = True
                try:
                    # Try to decode data as JSON, and register variables.
                    def reference_variables_in_dict(o):
                        for k in o.keys():
                            o[k] = reference_variables(o[k], quote=False)
                        return o
                    body = json.loads(data, object_hook=reference_variables_in_dict)
                except ValueError as ex:
                    pass
                except json.decoder.JSONDecodeError as ex:
                    data_is_json = False
                    pass
                if (not body) and (not data_is_json):
                    if '=' in data:
                        # data looks x-www-form-urlencoded
                        unique_params = set()
                        for kv in data.split('&'):
                            k, v = map(urllib.parse.unquote, kv.split('=', 1))
                            if k in unique_params:
                                # Requests will assume that only one parameter with a certain name can exist.
                                raise KeyError(
                                        f'Requests will assume that only one parameter with a certain name can exist, but we found more than one definition of {k!r}')
                            unique_params.add(k)
                            data[k] = reference_variables(v)
                if not body:
                    # No fancy interpretation of data was possible. Just pass the raw data.
                    body = reference_variables(data)
            if postman_auth := postman_request.get('auth', dict()):
                if auth_type := postman_auth.get('type'):
                    if auth_details := postman_auth.get(auth_type):
                        comments.append(f'{auth_type} auth: {auth_details!r}')
            postman_headers = postman_request.get('header', [])
            if postman_headers:
                for header in postman_headers:
                    k = header.get('key')
                    v = reference_variables(header.get('value'), quote=False)
                    header_type = header.get('type')
                    if header_type and header_type not in ('text', ):
                        raise NotImplementedError(f'Unknown header type: {header!r}')
                    if k == 'Host' and v == url_domain:
                        # Don't explicitly set Host header if it's the same as the host from the URL.
                        continue
                    if k == 'Connection' and v == 'close':
                        # Let Requests choose the TCP connection setting.
                        continue
                    if k in ('Content-Length',):
                        # Let Requests calculate the content length after it has serialised the request body.
                        continue
                    if variable_name := header_variables.get(v):
                        headers[k] = scaffolding.VariableReference(variable_name)
                    else:
                        headers[k] = v

            request = scaffolding.ScriptedRequest(
                verb = postman_request.get('method', 'get'),
                url = reference_variables(postman_request.get('url', dict()).get('raw', ''), quote=False),
                headers = headers,
                data = body,
                data_is_binary = isinstance(body, bytes),
                files = files,
                comment = comments,
                save_response_vars = dict(),
                )
            script.requests.append(request)
    parse_postman_item_list(postman_collection.get('item', []))

    if args.user:
        script.set_option('auth', tuple(args.user.split(':', 1)))

    cookie = args.cookie
    if cookie:
        cookie_creations = []
        for key_value in re.split(r';\s*', cookie):
            cookie_name, cookie_value = re.split(r'\s*=\s*', key_value, maxsplit=1)
            import_lines.add('import requests')
            cookie_creations.append(f'''requests.cookies.create_cookie(domain='{url_domain}', name='{cookie_name}', value='{cookie_value}')''')
        script.set_option('cookies', f'''[{', '.join(cookie_creations)}]''')

    if args.proxy:
        script.set_option('proxy', args.proxy)
        if args.proxy != 'http://127.0.0.1:8080':
            script.set_option('proxy', args.proxy, comment=repr('http://127.0.0.1:8080'))
    else:
        script.set_option('proxy', 'http://127.0.0.1:8080', commented_out=True)

    return str(script)

