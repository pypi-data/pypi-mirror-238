
from contextlib import contextmanager
from collections import namedtuple
from urllib.parse import urlparse
from datetime import timedelta
from pathlib import Path
from logging import *
import dataclasses
import traceback
import inspect
import socket
import types
import json
import time
import sys
import re

import redis

NOT_USED = object()

def my_exchandler(type, error, source):
    if getattr(error, 'response', None):
        print(error.response)
    elif getattr(error, 'document', None):
        print(error.document)
    # Strip the tail of the traceback for the boring part.
    def add_relevant_frame(tb_this):
        if tb_this.tb_frame == source.frame:
            return  types.TracebackType(tb_next=None,
                                          tb_frame=source.frame,
                                          tb_lasti=source.frame.f_lasti,
                                          tb_lineno=source.frame.f_lineno)
        tb_this.tb_next = add_relevant_frame(tb_this.tb_next)
        return tb_this
    error.__traceback__ = add_relevant_frame(error.__traceback__)
    traceback.print_exception(error)
@contextmanager
def except_handler(exc_handler):
    "Sets a custom exception handler for the scope of a 'with' block."
    sys.excepthook = exc_handler
    yield
    sys.excepthook = sys.__excepthook__

@dataclasses.dataclass
class BreakageError(Exception):
    message: str
    expectation_location: str
    expectation_context: str
    hostname: str = socket.gethostname()
    program: str = sys.argv[0]
    response: None = None
    document: None = None

    def __post_init__(self):
        super().__init__(self.message)

    def asdict(self):
        return {
                'message': self.message,
                'expectation_location': self.expectation_location,
                'expectation_context': self.expectation_context,
                'hostname': self.hostname,
                'program': self.program,
                }


def get_redis_connection():
    for host in (
            None,
            '127.0.0.1',
            'redis',
            ):
        r = redis.StrictRedis(host=host, decode_responses=True)
        try:
            r.ping()
            return r
        except:
            debug(f'No Redis found on host {host}. Maybe it\'s somewhere else?')


class WebClient:
    def __init__(self, force_wait_interval=timedelta(seconds=0), logging_level=DEBUG, health_alert_report_url=NOT_USED, health_alert_report_mute_seconds=NOT_USED, breakage_handler=None):
        self.breakage_handler = breakage_handler
        self.logger = getLogger(str(id(self)))
        self.logger.setLevel(logging_level)
        ch = StreamHandler()
        self.logger.addHandler(ch)
        self.r = get_redis_connection()
        if not (health_alert_report_url == NOT_USED and health_alert_report_mute_seconds == NOT_USED):
            self.logger.warning(f'Use of health alerts is deprecated. Please use breakage_handler on {source_line().location}')
        if type(force_wait_interval) == timedelta:
            self.force_wait_interval_seconds = int(force_wait_interval.total_seconds())
        else:
            self.force_wait_interval_seconds = int(force_wait_interval)


    def _sleep_for_holdoff(self, url):
        netloc = urlparse(url)[1]
        holdoff_key = f'ahi:holdoff:{netloc}'
        if self.r and self.force_wait_interval_seconds:
            holdoff_was_already_set = not bool(self.r.set(holdoff_key, 1, ex=self.force_wait_interval_seconds, nx=True))
            if holdoff_was_already_set:
                holdoff_seconds = float(self.r.ttl(holdoff_key))
                self.logger.info(f'{netloc} was recently hit. Holding off for {holdoff_seconds} seconds.')
                time.sleep(holdoff_seconds)
                # Set the marker now that we can.
                # If we don't do this, then:
                # Request 1 will go immediately, setting the marker
                # Request 2 will wait and then go
                # Request 3 will not see a marker and will go immediately (and set a marker)
                self.r.set(holdoff_key, 1, ex=self.force_wait_interval_seconds)


    def expect(self, expectation, message=None, value=None, response=None, document=None):
        '''Check if <expectation> is met. If not, a BreakageError is raised with <message>.

        If called with a lambda function as <expectation>, the lambda function is called with <value> as argument, and is expected to return a bool.
        If called with a type as <expectation>, this function checks if <value> is of that type.
        If called with anything else as <expectation>, this function only checks if that <expectation> is comparable to True.
        '''
        expectation_met = True
        expectation_location = None
        
        if isinstance(expectation, (type(lambda:_), type(self.expect), type(parses_as_json))):
            # expectation is a callable.
            if not expectation(value):
                expectation_met = False
                expectation_context = inspect.getsource(expectation)
        elif type(expectation) == type(int):
            # expectation is a type.
            if not isinstance(value, expectation):
                expectation_met = False
                expectation_context = f'{value} is a {type(value).__name__}, not a {expectation.__name__}'
                expectation_location = source_line().location
        else:
            # expectation is a bool.
            if not expectation:
                expectation_met = False
                caller_source = source_line()
                expectation_context = caller_source.code
                expectation_location = caller_source.location

        if not expectation_met:
            expectation_statement_match = re.search(r'expect\((.*)\)', expectation_context)
            if expectation_statement_match:
                expectation_context = expectation_statement_match.group(1)
            expectation_context = expectation_context.strip()
            location_text = expectation_location and f'at {expectation_location}' or 'here'

            # Fire API breakage event handler.
            error = BreakageError(
                    message or f'Failed to meet expectation {location_text}: {expectation_context}',
                    expectation_location = expectation_location,
                    expectation_context = expectation_context,
                    response = response,
                    document = document,
                    )
            if self.breakage_handler:
                self.breakage_handler(error)

            # You can expect (pun intended) this function to throw Exceptions often.
            # Reconstruct a traceback leading up to the user's line of source code (not this function),
            # for optimal readability.
            source = source_line()
            with except_handler(lambda type, error, error_traceback: my_exchandler(type, error, source)):
                raise error


SourceLine = namedtuple('SourceLine', ['location', 'code', 'frame'])
def source_line():
    stack = inspect.stack()
    try:
        this_frame = stack[0]
        ahi_package_dir = Path(this_frame.filename).parent
        for frame in stack:
            if Path(frame.filename).is_relative_to(ahi_package_dir):
                # Path is inside this package directory. Skip frame, go deeper.
                continue
            try:
                code = ''.join(frame.code_context)
            except TypeError:
                if frame.code_context:
                    code = str(frame.code_context)
                else:
                    code = '<no code available>'
            return SourceLine(f'{frame.filename} line {frame.lineno}', code, frame.frame)
    finally:
        del stack


def parses_as_json(text):
    '''Test if 'text' is parsable as JSON.'''
    try:
        json.loads(text)
        return True
    except json.decoder.JSONDecodeError:
        return False

