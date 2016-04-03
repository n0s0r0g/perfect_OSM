import os

import urllib
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from handlers.simplehandler import SimpleHandler

_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
_TIMEOUT = 10

_WEBSITE_NOT_AVAIL = """Сайт, указанный в теге website=* недоступен."""


class WebsiteChecker(SimpleHandler):
    def __init__(self):
        self._checked = dict()
        self._not_avail = list()

    def _check_url(self, url):
        if url in self._checked:
            return self._checked[url]

        status = False

        try:
            scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
            if scheme == '':
                scheme, netloc, path, query, fragment = urllib.parse.urlsplit('http://' + url)

            if ':' in netloc:
                host, port = netloc.split(':')
                # support for International domains
                host = host.encode('idna').decode('utf-8')
                netloc = host + ':' + port
            else:
                netloc = netloc.encode('idna').decode('latin-1')
            path = urllib.parse.quote(path)

            p_url = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))
            req = Request(p_url, headers={'User-Agent': _USER_AGENT})
            urlopen(req, None, _TIMEOUT)
        except HTTPError as e:
            if e.code == 301:  # permanent redirect
                status = True
        except:
            pass
        else:
            status = True

        self._checked[url] = status
        return status

    def process(self, item):
        if 'website' in item:
            if not self._check_url(item['website']):
                self._not_avail.append((item['tag'], item['id']))

    def finish(self, output_dir):
        if self._not_avail:
            fn = output_dir + 'errors/website/not_available/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_WEBSITE_NOT_AVAIL)

            fn = output_dir + 'errors/website/not_available/items.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                for item_tag, item_id in self._not_avail:
                    f.write('https://www.openstreetmap.org/%s/%d\n' % (item_tag, item_id))
