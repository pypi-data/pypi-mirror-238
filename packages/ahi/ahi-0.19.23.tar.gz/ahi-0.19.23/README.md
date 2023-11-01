# Application Hacking Interface

## Using the simple HTTPClient
```python
from logging import *
c = ahi.HTTPClient(cache_ttl=60, force_wait_interval=1, auto_adjust_for_rate_limiting=True, logging_level=DEBUG, proxy='http://127.0.0.1:8080', verify=True, allow_redirects=False, timeout=None)
resp = c.get('http://example.com/')
print(resp)
```

## Using the Selenium driver for Firefox
```python
from logging import *
from selenium.webdriver.common.keys import Keys
ff = ahi.SeleniumFirefox(headless=True, force_wait_interval=timedelta(seconds=0), logging_level=DEBUG)
ff.get('https://example.com/')
ff.html.css('#LoginForm_Password').send_keys('P4$$w0rd')
ff.html.css('#LoginForm_Password').send_keys(Keys.RETURN)
ff.execute_script('''SetLocation('\x2Fdocs\x2FProMyPlanning.aspx?_Division_=549942',event, 0)''')
ff.html.css('#Reports_Reports_Reports_MyPlanning').click()
print(ff.html)
```

## Converting from a curl command line
```bash
girl --curl https://example.com/
```
