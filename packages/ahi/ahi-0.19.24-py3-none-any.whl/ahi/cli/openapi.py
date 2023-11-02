
import urllib.parse
import pprint
import json
import re

from .. import response
from . import scaffolding

def openapi_to_ahi_code(args):
    '''Convert OpenAPI JSON to Python code using ahi.
    '''

    with open(args.openapi, 'r') as f:
        openapi = json.load(f)

    script = scaffolding.Script()
    script.set_option('verify', args.insecure)

    script.variables = dict()
    script.missing_variables = set()
    url_domain = None
    if args.url:
        # Let command line parameter overwrite the URL.
        url_scheme = urllib.parse.urlparse(args.url).scheme
        url_netloc = urllib.parse.urlparse(args.url).netloc
        script.variables['url_base'] = repr(f'{url_scheme}://{url_netloc}')
        url_domain = url_netloc.split(':')[0]
    elif servers := openapi.pop('servers', None):
        url_bases = list(filter(bool, [server.get('url') for server in servers]))
        if len(url_bases) == 1:
            script.variables['url_base'] = url_bases[0]
        elif len(url_bases) > 1:
            script.variables['url_base'] = '(' + ' | '.join(url_bases) + ')'
        else:
            script.variables['url_base'] = f'# {servers}'

    def dereference(mystery):
        match mystery:
            case {'$ref': schema_reference}:
                o = openapi
                for key in schema_reference.strip('#/').split('/'):
                    if not (o := o.get(key)):
                        raise KeyError(
                                f'Could not find {ref} in file')
                mystery = dereference(o)

        match mystery:
            case dict():
                o = dict()
                for k, v in mystery.items():
                    o[k] = dereference(v)
            case list():
                o = [dereference(i) for i in mystery]
            case _:
                o = mystery

        return o

    def pythonise(o, var_name=None):
        if var_name:
            script.missing_variables.add(var_name)
        match o:
            case {'type': 'object', 'properties': d}:
                o = {k: pythonise(v, var_name=k) for k, v in d.items()}
            case {'type': 'integer'}:
                o = scaffolding.VariableReference(f'int({scaffolding.pythonise_var_name(var_name)})')
            case {'type': 'string', 'format': 'binary'}:
                o = scaffolding.VariableReference(f'bytes({scaffolding.pythonise_var_name(var_name)})')
            case {'type': 'string', 'enum': list(enum_options)}:
                o = scaffolding.VariableReference('(' + ' | '.join(map(repr, enum_options)) + ')')
                # We just hardcoded the enum options. No need to register a missing variable.
                script.missing_variables.remove(var_name)
            case {'type': 'string'}:
                o = scaffolding.VariableReference(f'str({scaffolding.pythonise_var_name(var_name)})')
            case {'type': 'boolean'}:
                o = scaffolding.VariableReference(f'bool({scaffolding.pythonise_var_name(var_name)})')
            case _:
                raise NotImplementedError(
                        f'Cannot parse {o!r}')
        return o

    def extraction_code(o, var_name_prefix='', var_name='', extraction_code_prefix=''):
        def name(var):
            return scaffolding.pythonise_var_name(f'{var_name_prefix} {var}')
        python_type = None
        match o:
            case {'type': 'object', 'properties': d}:
                for k, v in d.items():
                    if k:
                        yield from extraction_code(v, var_name_prefix=name(k), var_name=k, extraction_code_prefix=extraction_code_prefix+f".get('{k}')")
            case {'type': 'integer'}:
                python_type = 'int'
            case {'type': 'string', 'format': 'binary'}:
                python_type = 'bytes'
            case {'type': 'string'}:
                python_type = 'str'
            case {'type': 'boolean'}:
                python_type = 'bool'
            case {'items': items, 'type': 'array'}:
                loop_code = f'for item in {extraction_code_prefix}:\n'
                match items:
                    case {'properties': item_properties, 'type': 'object'}:
                        for sub_var_name, sub_extraction_code in extraction_code(items, var_name_prefix=name('item'), extraction_code_prefix='item'):
                            yield (f'{loop_code}    {sub_var_name}', sub_extraction_code)
                            loop_code = ''
                    case _:
                        pprint.pprint(items)
                        raise NotImplementedError(
                                f'Unable to generate variable extraction code for array {var_name_prefix}')
            case _:
                pprint.pprint(o)
                raise NotImplementedError(
                        f'Unable to generate variable extraction code for {var_name_prefix}')
        if python_type:
            if re.search(f"\\.get\('{var_name}'\)$", extraction_code_prefix):
                extraction_code_prefix = re.sub(f"\\.get\('{var_name}'\)$", f".get('{var_name}', expect={python_type})", extraction_code_prefix)
                yield (var_name_prefix, scaffolding.VariableReference(extraction_code_prefix))
            else:
                yield (var_name_prefix, scaffolding.VariableReference(f'{python_type}({extraction_code_prefix})'))

    def add_request(method, path, content_type=None, body=None, operation_id=None, description=None, headers=response.HeadersCollection(dict(), None), comments=list(), save_response_vars=dict):
        url = scaffolding.VariableReference(f"f'{{url_base}}{path}'")
        script.missing_variables.add('url_base')
        if content_type:
            headers['Content-Type'] = content_type
        if description:
            comments.insert(0, description)
        if operation_id:
            comments.insert(0, operation_id)
        request = scaffolding.ScriptedRequest(
                verb = method,
                url = url,
                headers = headers,
                data = body,
                data_is_binary = isinstance(body, bytes),
                comment = comments,
                save_response_vars = save_response_vars,
                )
        script.requests.append(request)

    for path, path_info in openapi.get('paths', dict()).items():
        path_comments = list()
        # Warning: OpenAPI parameter definitions can also be on the method level. (See below.))
        for parameter in path_info.pop('parameters', []):
            match parameter:
                case {'description': str(parameter_description),
                      'in': str(position),
                      'name': str(parameter_name),
                      'required': bool(required_parameter),
                      'schema': {'type': str(parameter_type)}}:
                    path_comments.append(f'{required_parameter and "required " or ""}{parameter_type} {position} parameter "{parameter_name}": {parameter_description}')
                    script.missing_variables.add(parameter_name)
                case _:
                    pprint.pprint(parameter)


        for method, method_info in path_info.items():
            headers = response.HeadersCollection(dict(), None)
            method_comments = list()
            save_response_vars = dict()
            if not isinstance(method_info, dict):
                pprint.pprint(method_info)
                raise NotImplementedError(
                        f'{path} {method} method info is a {type(method_info).__name__}, not a dict')
            operation_id = method_info.pop('operationId')
            for response_name, expected_response in method_info.pop('responses', dict()).items():
                var_prefix = scaffolding.pythonise_var_name(operation_id + ' ' + expected_response.pop('description', response_name))
                if not expected_response:
                    continue
                match expected_response_content := expected_response.pop('content', None):
                    case {'application/json': {'schema': schema}}:
                        save_response_vars = dict(extraction_code(dereference(schema), var_name_prefix=var_prefix, extraction_code_prefix='resp.json'))
                    case _:
                        pprint.pprint(expected_response)
                        raise NotImplementedError(
                                f'Unknown expected "{response_name}" response definition.')
            
            # Warning: OpenAPI parameter definitions can also be on the path level. (See above.)
            for parameter in method_info.pop('parameters', []):
                match parameter:
                    case {'description': str(parameter_description),
                          'in': str(position),
                          'name': str(parameter_name),
                          'required': bool(required_parameter),
                          'schema': {'type': str(parameter_type)}}:
                        method_comments.append(f'{required_parameter and "required " or ""}{parameter_type} {position} parameter "{parameter_name}": {parameter_description}')
                        script.missing_variables.add(parameter_name)
                    case _:
                        pprint.pprint(parameter)
                        raise NotImplementedError(
                                f'Unknown parameter definition')
            
            if security_info := method_info.pop('security', None):
                # [{'Bearer': []}]
                for security_option in security_info:
                    match security_option:
                        case {'Bearer': value}:
                            if value:
                                headers['Authorization'] = f'Bearer {value}'
                            else:
                                headers['Authorization'] = scaffolding.VariableReference("f'Bearer {bearer_token}'")
                            script.missing_variables.add('bearer_token')
                        case _:
                            pprint.pprint(security_option)
                            raise NotImplementedError(
                                    f'Unknown security option format')

            description = ' - '.join(list(filter(bool, [method_info.pop('summary', None), method_info.pop('description', None)])))
            method_comments.extend(method_info.pop('tags', []))

            if request_body := method_info.pop('requestBody', None):
                if body_description := request_body.pop('description', None):
                    method_comments.append(body_description)
                for content_type, content in request_body.pop('content', dict()).items():
                    match content:
                        case {'schema': schema_reference}:
                            o = dereference(schema_reference)
                            body = pythonise(o)
                            add_request(method, path, content_type=content_type, headers=headers, body=body, operation_id=operation_id, description=description, comments=path_comments+method_comments, save_response_vars=save_response_vars)
                        case _:
                            pprint.pprint(content)
                            raise NotImplementedError(
                                    f'Unknown request body content definition')
                if request_body:
                    pprint.pprint(request_body)
                    raise NotImplementedError(
                            f'Unknown request body definition parts')
            else:
                add_request(method, path, headers=headers, operation_id=operation_id, description=description, comments=path_comments+method_comments, save_response_vars=save_response_vars)
            if method_info:
                pprint.pprint(method_info)
                raise NotImplementedError(
                        f'Unknown extra info')

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

