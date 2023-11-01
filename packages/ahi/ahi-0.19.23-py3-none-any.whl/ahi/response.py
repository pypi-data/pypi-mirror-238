#!/usr/bin/env python

from urllib.parse import urljoin
from logging import *
import warnings
import base64
import types
import html
import json
import re

import parsel

from . import common

_meta_tag_url_rex = re.compile(r'(?i)(?<=url=)\S+')
MAX_CACHE_CONTENT_SIZE = 1024 * 1024


def _maybe_wrap(native, client):
    if isinstance(native, dict):
        return DictFacade(native, client)
    elif isinstance(native, list):
        return ListFacade(native, client)
    return native


def _unwrap(facade):
    if isinstance(facade, IterableFacade):
        return facade.native
    return facade


class FacadeIterator():
    def __init__(self, native_iterator, client):
        self._client = client
        self._native_iterator = native_iterator


    def __iter__(self):
        # This function is here because apparently, the standard library json.dump() implementation
        # expects an iterator to be iterable itself.
        return self

    def __next__(self):
        nxt = self._native_iterator.__next__()
        return _maybe_wrap(nxt, self._client)


class IterableFacade:
    def __init__(self, native, client):
        self._client = client
        super().__init__(native)


    def __iter__(self):
        return FacadeIterator(super().__iter__(), self._client)


    def __getattr__(self, name):
        self._client.expect(False, f'Expected {self!r} to have attribute "{name}", which does not exist on {type(self).__name__} (possible type confusion after API breakage)')


class ListFacade(IterableFacade, list):
    @property
    def native(self):
        '''A Python native list instead of this facade class.'''
        return [_unwrap(e) for e in self]


class DictFacade(IterableFacade, dict):
    def __getitem__(self, key):
        if self._client:
            self._client.expect(key in self.keys(), f'Expected key "{key}" in dict, but only found {list(self.keys())}')
        return _maybe_wrap(super().__getitem__(key), self._client)
    

    def get(self, key, default=None, case_sensitive=True, expect=common.NOT_USED):
        if type(expect) == bool and expect and self._client:
            self._client.expect(key in self.keys(), f'Expected key "{key}" in dict, but only found {list(self.keys())}')
        if case_sensitive:
            value = _maybe_wrap(super().get(key, default), self._client)
        else:
            matches = dict()
            for k, v in self.items():
                if k.casefold() == key.casefold():
                    matches[k] = v
                    value = v
            if not matches:
                value = default
            elif len(matches) > 1:
                raise KeyError(
                        f'Multiple matches for case insensitive {key!r}: {tuple(matches.keys())}')
        if expect != common.NOT_USED and self._client:
            if type(expect) == type(int):
                self._client.expect(expect, value=value, message=f'Expected key "{key}" to be a {expect.__name__}, but found {value!r}')
            elif type(expect) != bool:
                self._client.expect(expect, value=value)
        if self._client and key in self.keys() and expect == common.NOT_USED:
            type_name = {
                    DictFacade: 'dict',
                    ListFacade: 'list',
                    }.get(type(value), type(value).__name__)
            self._client.logger.debug(f'Key "{key}" found. Get automatically alerted of data structure changes by using get(\'{key}\', expect={type_name}) on {common.source_line().location}')
        return value

    
    def pop(self, key, default=common.NOT_USED, expect=common.NOT_USED):
        if default == common.NOT_USED and expect != False:
            value = self[key]
        else:
            value = self.get(key, default=default, expect=expect)
        if key in self.keys():
            del self[key]
        return value


    def values(self):
        return _maybe_wrap(list(super().values()), self._client)
    

    def items(self):
        return [(_maybe_wrap(k, self._client), _maybe_wrap(v, self._client)) for k, v in super().items()]


    @property
    def native(self):
        '''A Python native dict instead of this facade class.'''
        return {_unwrap(k): _unwrap(v) for k, v in super().items()}


class HeadersCollection(DictFacade):
    def __getitem__(self, key):
        value = self.get(key)
        if value == None:
            if self._client:
                self._client.expect(key in self.keys(), f'Expected key "{key}" in dict, but only found {list(self.keys())}')
            else:
                # Trigger base class exception.
                return super()[key]
        return _maybe_wrap(value, self._client)
    

    def get(self, key, default=None, expect=common.NOT_USED):
        return super().get(key, default=default, case_sensitive=False, expect=expect)


    def __str__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.items()])


class URLCollectionIterator():
    def __init__(self, urls):
        self._set_iterator = urls.__iter__()


    def __next__(self):
        next_tuple = self._set_iterator.__next__()
        return next_tuple[0]


class URLCollection():
    def __init__(self):
        self._urls = set()


    def __len__(self):
        return len(self._urls)


    def add(self, url, relative_to='', html_unescape=True, normalise_url=True):
        '''Add a URL to the collection.

        URL 'url' (which may be relative to 'relative_to' is added to the collection.
        In the process, HTML unescaping may be enabled using 'html.unescape()' (input: &lt; output: <),
        as well as URL normalisation using 'urllib.urlparse.urljoin()' (input: /foo.html relative to http://example.com/bar/ output: http://example.com/foo.html).
        '''
        if html_unescape:
            url = html.unescape(url)
            relative_to = html.unescape(relative_to)
        if normalise_url:
            url = urljoin(relative_to, url)
            relative_to = ''
        self._urls.add((url, relative_to))


    def __iter__(self):
        '''Return a URLCollectionIterator object to iterate over the URLs in the collection.
        
        The elements returned by the iterator are all of type str.
        '''
        return URLCollectionIterator(self._urls)


    def normalise(self):
        '''Return a new collection with all URLs normalised.

        Applies URL normalisation using 'urllib.urlparse.urljoin()' (input: /foo.html relative to http://example.com/bar/ output: http://example.com/foo.html).
        '''
        result = URLCollection()
        for url, relative_to in self._urls:
            result.add(urljoin(relative_to, url), html_unescape=False)
        return result


    def matching_regex(self, expression: str):
        '''Return a new collection with all URLs that (when normalised) match the regex 'expression'.'''
        rex = re.compile(expression)
        result = URLCollection()
        for url, relative_to in self._urls:
            if rex.search(urljoin(relative_to, url)):
                result.add(url, relative_to, html_unescape=False)
        return result

    def http_or_https(self):
        '''Return a new collection with all URLs that (when normalised) match the regex ^(http(s):)?//'''
        return self.matching_regex('^(http(s):)?//')


    def __str__(self):
        return '\n'.join(sorted(self))


class Document():
    def __init__(self, url, text, client):
        '''Create a Document with 'text' that came from 'url'.'''
        self.url = url
        self.text = text
        self._client = client

    
    @property
    def _selector(self):
        return parsel.Selector(self.text)


    def css(self, query, expect=common.NOT_USED):
        '''Find HTML elements using a CSS selector query.

        This is one of the functions that are wrapped from a Selector object from the parsel library.
        For usage, see https://parsel.readthedocs.io/en/latest/usage.html
        '''
        selected = self._selector.css(query)
        if type(expect) == bool and expect and self._client:
            self._client.expect(selected, f'Did not find expected HTML matching CSS selector "{query}" on {self.url}', document=self)
        if type(expect) != bool and expect != common.NOT_USED and self._client:
            self._client.expect(expect, value=selected)
        if self._client and expect == common.NOT_USED and selected:
            self._client.logger.debug(f'Results found for css(\'{query}\'). Get automatically alerted of HTML changes by using css(\'{query}\', expect=True) on {common.source_line().location}')
        return selected


    def xpath(self, query, namespaces=None, expect=common.NOT_USED, **kwargs):
        '''Find HTML elements using an XPath expression.

        This is one of the functions that are wrapped from a Selector object from the parsel library.
        For usage, see https://parsel.readthedocs.io/en/latest/usage.html
        '''
        warnings.warn('xpath() will be removed from this library. Please use css() instead.', DeprecationWarning, stacklevel=2)

        selected = self._selector.xpath(query, namespaces, **kwargs)
        if type(expect) == bool and expect and self._client:
            self._client.expect(selected, f'Did not find expected HTML matching XPath selector "{query}" on {self.url}', document=self)
        if type(expect) != bool and expect != common.NOT_USED and self._client:
            self._client.expect(expect, value=selected)
        if self._client and expect == common.NOT_USED and selected:
            self._client.logger.debug(f'Results found for xpath(\'{query}\'). Get automatically alerted of HTML changes by using xpath(\'{query}\', expect=True) on {common.source_line().location}')
        return selected


    def re(self, regex, expect=common.NOT_USED):
        results = re.findall(regex, self.text)
        if type(expect) == bool and expect and self._client:
            self._client.expect(results, f'Did not find expected HTML matching regex {regex!r} on {self.url}', document=self)
        if type(expect) != bool and expect != common.NOT_USED and self._client:
            self._client.expect(expect, value=selected)
        if self._client and expect == common.NOT_USED and results:
            self._client.logger.debug(f'Results found for re({regex!r}). Get automatically alerted of HTML changes by using re({regex!r}, expect=True) on {common.source_line().location}')
        return results


    @property
    def links(self):
        '''Return the URLs found in <a href="..."> elements.

        This should be the collection of URLs that the author of the document could expect you to navigate to.
        See also 'Document.urls'.'''
        selector = parsel.Selector(self.text)
        results = URLCollection()
        for e in selector.css('a[href]'):
            results.add(e.attrib['href'], relative_to=self.url)
        return results


    @property
    def urls(self):
        '''Return all the URLs that may be found in this 'Document' using a generic algorithm.

        URLs are scraped from all HTML elements defining attributes such as "href", "src" or "action",
        as well as <object> tags with a "data" attribute.
        On top of that, the 'Document' text is searched for strings matching the regex https?://[^"'\s);<>]+
        This should be a fairly complete collection of URLs mentioned in the document, not all of which necessarily
        should be expected to be navigable.
        See also 'Document.links'
        '''
        selector = parsel.Selector(self.text)
        results = self.links
        for attribute in ('href',
                          'src',
                          'action',
                          'background',
                          'formaction',
                          'manifest',
                          'poster',
                          ):
            for e in selector.css(f'[{attribute}]'):
                results.add(e.attrib[attribute], relative_to=self.url)
        for e in selector.css('object[data]'):
            results.add(e.attrib['data'], relative_to=self.url)
        # TODO: Improve regex.
        for url_match in re.finditer(r'''https?://[^"'\s);<>]+''', self.text):
            results.add(url_match.group(0), relative_to=self.url)
        return results


    def __str__(self):
        return self.text


class Response():
    def __init__(self, serialised_cached_response=None, requests_library_response=None, ahi_client=None, url=None):
        self.from_cache = bool(serialised_cached_response)
        self._cached_data = dict()
        self.url = url
        self._ahi_client = ahi_client
        if serialised_cached_response:
            self.requests_library_response = None

            self._cached_data = json.loads(serialised_cached_response)
            self.status_code = self._cached_data.get('status_code')
            self.reason = self._cached_data.get('reason')
            self.headers = HeadersCollection(self._cached_data.get('headers'), None)
        elif requests_library_response != None:
            self.requests_library_response = requests_library_response

            self.status_code = requests_library_response.status_code
            self.ok = requests_library_response.ok
            self.reason = requests_library_response.reason
            self.headers = HeadersCollection(requests_library_response.headers, self._ahi_client)
        else:
            raise RuntimeError('Response objects need to be created from either cached responses or fresh requests library response objects.')


    def __len__(self):
        '''Get the length of the response body.'''
        # Do not trigger a (potentially massive) download if we just want to check the size.
        if self._cached_data.get('binary'):
            return len(self._binary)
        elif self._cached_data.get('text'):
            return len(self.text)
        else:
            # No content available client side yet. Check the header.
            content_length = self.headers.get('Content-Length', expect=False)
            if content_length:
                return int(content_length)
            else:
                # Header not available. Download and check binary content first.
                if self._binary:
                    return len(self._binary)
                elif self.text:
                    return len(self.text)
                #raise RuntimeError(f'{repr(self)} has no body and no Content-Length header')
                return 0


    def __str__(self):
        body = ''
        if self.text:
            body = '\n'
            try:
                body += json.dumps(self.json, sort_keys=True, indent=4)
            except:
                body += self.text
        return f'{self.status_code} {self.reason}\n{self.headers}\n{body}'


    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.status_code}]>'


    def getcode(self):
        return self.status_code
    @property
    def status(self):
        return self.status_code
    @property
    def code(self):
        return self.status_code
    def getstatus(self):
        return self.status_code



    @property
    def _binary(self):
        cached_binary_base64 = self._cached_data.get('binary')
        if cached_binary_base64:
            return base64.b64decode(cached_binary_base64.encode())


    def raise_for_status(self):
        if self.requests_library_response != None:
            if self._client:
                self._client.expect(self.ok, f'Expected response on {self.url} to be OK, but got {self.status_code} {self.reason}', response=self)
            return self.requests_library_response.raise_for_status()


    @property
    def text(self):
        '''The string representing the current Response body.
        '''
        if (not self._cached_data) and self.requests_library_response != None:
            # Text was not cached yet. Cache it.
            # (For a binary body, this triggers a one-time download and consumption of self.requests_library_response.content,
            # which would disable reuse of self.text.)
            self._cached_data['text'] = self.requests_library_response.text
        return self._cached_data.get('text')


    def read(self):
        return self.content


    @property
    def content(self):
        '''Access the response body as bytes, for non-text requests.
        '''
        # Try to serve from cache.
        cached_binary = self._binary
        if cached_binary:
            return cached_binary
        
        if (not self._cached_data) and self.requests_library_response != None:
            # No cache. Download chunks and put together.
            content = bytes()
            for chunk in self.iter_content():
                content += chunk
            return content


    @property
    def json(self):
        '''The current Response body, decoded as JSON.
        '''
        try:
            o = json.loads(self.text)
            o = _maybe_wrap(o, self._ahi_client)
            # Generate a new type on the fly, to ba able to add a __call__ implementation.
            wrappable_class = type(o)
            cls = types.new_class(f'callable_{wrappable_class.__name__}', (wrappable_class,))
            # This makes ahi code more compatible with requests code. These behave alike:
            # requests.get(url).json()
            # ahi.get(url).json()
            # ahi.get(url).json
            cls.__call__ = lambda self: self
            if issubclass(cls, dict) or issubclass(cls, list):
                return cls(o, self._ahi_client)
            else:
                return cls(o)
        except Exception as ex:
            description = f'{ex} while expecting to be able to deserialise response as JSON.'
            content_type = self.headers.get('Content-Type', expect=False)
            if content_type:
                description += f' (Hint: response Content-Type is "{content_type}")'
            if isinstance(ex, json.decoder.JSONDecodeError):
                snippet_start = ex.pos - 10
                snippet_end = min(ex.pos + 20, len(self.text))
                description += f' Decoding error occurred around here: {self.text[snippet_start:snippet_end]}'
            if self._ahi_client:
                self._ahi_client.expect(False, description, response=self)
            else:
                raise RuntimeError(description)


    @property
    def html(self):
        '''The Document representing the current Response body.
        '''
        return Document(self.url, self.text, self._ahi_client)


    def iter_content(self, chunk_size=1024):
        '''Iterate over the content of the response.

        Use this if you want to "download" a "file":
        with open(local_filename, 'wb') as f:
            for chunk in resp.iter_content(): 
                f.write(chunk)
        '''
        if self._binary != None:
            #debug(f'Iterating over cached binary data.')
            for offset in range(0, len(self._binary), chunk_size):
                chunk = self._binary[offset:offset+chunk_size]
                if chunk:
                    #debug(f'Downloaded {len(chunk)} bytes.')
                    yield chunk
        elif self.requests_library_response != None:
            #debug(f'Iterating over requests library response.')
            content = bytes()
            cache = len(self) < MAX_CACHE_CONTENT_SIZE
            for chunk in self.requests_library_response.iter_content(chunk_size=chunk_size):
                if chunk:
                    #debug(f'Downloaded {len(chunk)} bytes.')
                    if cache:
                        content += chunk
                    yield chunk
            if cache:
                self._cached_data['binary'] = base64.b64encode(content).decode()
        else:
            raise RuntimeError('Response data not available in binary form.')


    def serialise(self):
        d = {
            'status_code': self.status_code,
            'reason': self.reason,
            'headers': self.headers,
            }
        # FIXME: Max cachable body size is already checked in HTTPClient().request(). Only HTTPClient._check_endpoint_health() doesn't check yet. Probably should replace full response saving in _check_endpoint_health(). After that, remove the check here.
        if len(self.text) < MAX_CACHE_CONTENT_SIZE:
            d['text'] = self.text
            d['binary'] = base64.b64encode(b''.join(self.iter_content())).decode()
        return json.dumps(d)


    def html_form_to_request_input(self, form):
        '''Takes an HTML <form> element (as selected by parsel).
            Returns a dict: {verb:, url:, data:}
            One use case for this is to follow form-based redirects:
            resp = get('https://example.com/')
            form = resp.html.css('form')
            response_after_redirect = ahi.request(**(resp.html_form_to_request_input(form)))
        '''
        try:
            next_url = urljoin(self.url, form.attrib['action'])
        except KeyError:
            next_url = self.url
        form_method = (form.attrib['method'] or 'GET').upper()
        form_data = dict()
        for input_element in form.css('input'):
            try:
                form_field_name = input_element.attrib['name']
                try:
                    form_field_value = input_element.attrib['value']
                except KeyError:
                    form_field_value = ''
                form_data[form_field_name] = form_field_value
            except KeyError:
                warning(f'<input> element without name attribute: {input_element.get()}')
        return {'verb': form_method, 'url': next_url, 'data': form_data}


    def html_meta_redirect_to_request_input(self):
        '''Finds an HTML <meta> element in the current Response body.
            Returns a dict: {verb:, url:, data:}
            One use case for this is to follow form-based redirects:
            resp = get('https://example.com/')
            response_after_redirect = ahi.request(**(resp.html_meta_redirect_to_request_input()))
        '''
        selector = parsel.Selector(self.text)
        meta_tag = selector.css('meta[http-equiv="refresh"]')
        meta_tag_content = meta_tag.attrib.get('content')
        next_url_match = _meta_tag_url_rex.search(meta_tag_content)
        if not next_url_match:
            description = f'Expected a <meta> tag redirect URL, but could not find it in "{meta_tag.get()}"'
            if self._ahi_client:
                self._ahi_client.expect(False, description, response=self)
            else:
                raise RuntimeError(
                        description)
        else:
            next_url = next_url_match.group(0)
            return {'verb': 'GET', 'url': next_url, 'data': None}


