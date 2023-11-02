#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta
from logging import *
import time
import sys
import os
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import selenium.common.exceptions

from .response import Document
from . import selenium_firefox
from . import common


class SeleniumChrome(selenium_firefox.SeleniumFirefox):
    def __init__(self, headless=True, force_wait_interval=timedelta(seconds=0), timeout=selenium_firefox.PAGE_LOAD_TIMEOUT_SECONDS, logging_level=DEBUG, proxy=None, verify=None, health_alert_report_url=common.NOT_USED, health_alert_report_mute_seconds=common.NOT_USED, breakage_handler=None):
        '''
        headless:                           Run Chrome in headless mode. You will not be able to manually interact with the browser.
        force_wait_interval:                Hit the target host no more then once every so many seconds (or a datetime.timedelta). WARNING: this exclusively implements delays between calls to get(). Clicking elements, sending keystrokes and things like Javascript can still induce HTTP requests sooner than the set interval.
        timeout:                            The default timeout in seconds to use for CSS and regex selections.
        '''
        super().__init__(force_wait_interval=force_wait_interval, timeout=selenium_firefox.PAGE_LOAD_TIMEOUT_SECONDS, logging_level=logging_level, health_alert_report_url=health_alert_report_url, health_alert_report_mute_seconds=health_alert_report_mute_seconds, breakage_handler=breakage_handler)
        options = Options()
        # TODO: Set options like "always ask for download file location", see https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.firefox.options
        # TODO: Add parameters:
        # - health_alert_report_url
        # - health_alert_report_mute_seconds
        # TODO: Add more logging.

        # Chrome Headless mode prevents popping up windows, and enables running on systems without a monitor.
        options.headless = headless
        if verify == False:
            raise RuntimeError(f'Chrome does not support ignoring untrusted certificates. Try Firefox.')
        if proxy:
            raise RuntimeError(f'Chrome does not support proxies. Try HTTPClient')
        try:
            self._driver = webdriver.Chrome()#options=options)
        except selenium.common.exceptions.WebDriverException as ex:
            if str(ex).strip() == 'Message: invalid argument: can\'t kill an exited process':
                current_display = os.getenv('DISPLAY', '(not_set)')
                raise RuntimeError(f'Problem initialising chromedriver. Common causes: you don\'t have chromedriver installed, or you are running this program with environment variable DISPLAY={current_display} while your desktop is on another X display.')
            else:
                print(f'ex casted to string: "{ex}"')
                raise ex
        if type(force_wait_interval) == timedelta:
            self.force_wait_interval_seconds = int(force_wait_interval.total_seconds())
        else:
            self.force_wait_interval_seconds = int(force_wait_interval)

