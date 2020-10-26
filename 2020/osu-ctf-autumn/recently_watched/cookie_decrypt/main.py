from pycookiecheat import chrome_cookies
import requests

url = 'http://example.com/fake.html'

# Uses Chrome's default cookies filepath by default
cookies = chrome_cookies(url)
r = requests.get(url, cookies=cookies)
