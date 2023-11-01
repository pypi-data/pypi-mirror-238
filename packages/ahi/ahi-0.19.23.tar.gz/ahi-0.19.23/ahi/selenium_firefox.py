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
from . import common


PAGE_LOAD_TIMEOUT_SECONDS = 4
captcha_rex = re.compile(r'(?i)\<[^<]*?(?!</re)captcha[^>]*?\>')


class SeleniumDocument(Document):
    def __init__(self, client):
        self._client = client
        self._driver = client._driver


    @property
    def url(self):
        return self._driver.current_url


    @property
    def text(self):
        for _ in range(3):
            try:
                return self._driver.page_source
            except selenium.common.exceptions.WebDriverException as ex:
                if str(ex).strip() == 'Message: TypeError: curContainer.frame.document.documentElement is null':
                    time.sleep(1)
                else:
                    raise ex


    def css(self, query, timeout=None, parsel=False, one=True, expect=common.NOT_USED):
        '''Find HTML elements using a CSS selector query.

        This function wraps functions like find_element() from selenium.webdriver.
        Warning: this means that SeleniumDocument.css() returns different results than Document.css()! (Unless you pass parsel=True)
        For usage and the returned results, see: https://selenium-python.readthedocs.io/locating-elements.html#locating-elements-by-css-selectors
        Set 'one' to False to get an iterable of matched elements.
        When 'timeout' is None, the client's timeout will be used. Use 0 to disable timeout.
        For what else happens when you specify a 'timeout', see: https://selenium-python.readthedocs.io/waits.html#explicit-waits
        '''
        if parsel:
            return super().css(query)
        if timeout == None:
            timeout = self._client.timeout
        if timeout:
            # Timout specified. Wait for max. <timeout> seconds until the intended element appears.
            start_time = datetime.now()
            while datetime.now() < start_time + timedelta(timeout):
                try:
                    if WebDriverWait(self._driver, timeout).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, query))):
                        break
                except (selenium.common.exceptions.ElementClickInterceptedException, selenium.common.exceptions.ElementNotInteractableException):
                    # Elements may still be moving around, for instance.
                    pass
        results = self._driver.find_elements(by=By.CSS_SELECTOR, value=query)
        if type(expect) == bool and expect and self._client:
            self._client.expect(results, f'Did not find expected HTML matching CSS selector "{query}" on {self.url}', document=self)
        if self._client and expect == common.NOT_USED and results:
            self._client.logger.debug(f'Results found for css(\'{query}\'). Get automatically alerted of HTML changes by using css(\'{query}\', expect=True) on {common.source_line().location}')
        if one:
            for result in results:
                if type(expect) != bool and expect != common.NOT_USED and self._client:
                    self._client.expect(expect, value=result)
                return result
        else:
            if type(expect) != bool and expect != common.NOT_USED and self._client:
                self._client.expect(expect, value=results)
            return results



    def re(self, regex, timeout=None, expect=common.NOT_USED):
        self._client._deal_with_obstructions()
        start_time = datetime.now()
        if timeout == None:
            timeout = self._client.timeout
        while datetime.now() < start_time + timedelta(seconds=timeout):
            matches = super().re(regex, expect=expect)
            if matches:
                return matches


class SeleniumFirefox(common.WebClient):
    def __init__(self, headless=True, force_wait_interval=timedelta(seconds=0), timeout=PAGE_LOAD_TIMEOUT_SECONDS, logging_level=DEBUG, verify=True, health_alert_report_url=common.NOT_USED, health_alert_report_mute_seconds=common.NOT_USED, breakage_handler=None):
        '''
        headless:                           Run Firefox in headless mode. You will not be able to manually interact with the browser.
        force_wait_interval:                Hit the target host no more then once every so many seconds (or a datetime.timedelta). WARNING: this exclusively implements delays between calls to get(). Clicking elements, sending keystrokes and things like Javascript can still induce HTTP requests sooner than the set interval.
        timeout:                            The default timeout in seconds to use for CSS and regex selections.
        '''
        super().__init__(force_wait_interval=force_wait_interval, logging_level=logging_level, health_alert_report_url=health_alert_report_url, health_alert_report_mute_seconds=health_alert_report_mute_seconds, breakage_handler=breakage_handler)
        options = Options()
        # TODO: Add parameters:
        # - proxy
        # TODO: Add more logging.

        profile = webdriver.FirefoxProfile()
        # Set option "always ask for download file location".
        profile.set_preference('browser.download.useDownloadDir', False)

        # Firefox Headless mode prevents popping up windows, and enables running on systems without a monitor.
        self._headless = headless
        options.headless = headless
        options.accept_insecure_certs = not verify
        try:
            self._driver = webdriver.Firefox(options=options, firefox_profile=profile, log_path='/tmp/geckodriver.log')
        except selenium.common.exceptions.WebDriverException as ex:
            if str(ex).strip() == 'Message: invalid argument: can\'t kill an exited process':
                current_display = os.getenv('DISPLAY', '(not_set)')
                raise RuntimeError(f'Problem initialising geckodriver. Common causes: you don\'t have geckodriver installed, or you are running this program with environment variable DISPLAY={current_display} while your desktop is on another X display.')
            else:
                print(f'ex casted to string: "{ex}"')
                raise ex
        if type(force_wait_interval) == timedelta:
            self.force_wait_interval_seconds = int(force_wait_interval.total_seconds())
        else:
            self.force_wait_interval_seconds = int(force_wait_interval)
        self.timeout = timeout


    def get(self, url):
        self._sleep_for_holdoff(url)
        # TODO: Handle common errors?
        self._driver.get(url)
        self._deal_with_obstructions()

    @property
    def url(self):
        return self._driver.current_url
    @url.setter
    def url(self, new_url):
        self.get(new_url)

    @property
    def headless(self):
        return self._headless


    def _deal_with_obstructions(self):
        try:
            # See if there's a CAPTCHA in view.
            captcha_artifact = self.html.css('#recaptcha-verify-button', timeout=0)
            if captcha_artifact:
                self.expect(not self.headless, 'Unexpectedly ran into a CAPTCHA challenge while in headless mode')
                self.logger.warning(f'{sys.argv[0]} will continue after you solve the CAPTCHA: {captcha_artifact}')
                time.sleep(1)
            # Wait until the user solves the captcha.
            while captcha_artifact:
                self.logger.debug(f'{datetime.now()} {captcha_artifact}')
                time.sleep(1)
                captcha_artifact = self.html.css('#recaptcha-verify-button', timeout=0)
        except selenium.common.exceptions.NoSuchElementException:
            pass


    @property
    def text(self):
        return self.html.text


    @property
    def html(self):
        return SeleniumDocument(self)


    @property
    def cookies(self):
        return self._driver.get_cookies()

    
    def execute_script(self, *args, **kwargs):
        return self._driver.execute_script(*args, **kwargs)


    def __del__(self):
        if hasattr(self, '_driver'):
            self.logger.debug(f'Quitting {self}.')
            self._driver.quit()

