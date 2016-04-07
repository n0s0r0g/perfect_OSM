import urllib.error
import urllib.parse
import urllib.request

from handlers.simplehandler import SimpleHandler

_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
_TIMEOUT = 10

_DEAD_LINKS = """Сайт, указанный в теге website, contact:website, url или source_ref недоступен."""


class WebsiteChecker(SimpleHandler):
    def __init__(self):
        self._checked = dict()
        self._dead_links = list()

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
            req = urllib.request.Request(p_url, headers={'User-Agent': _USER_AGENT})
            urllib.request.urlopen(req, None, _TIMEOUT)
        except urllib.error.HTTPError as e:
            if e.code == 301:  # permanent redirect
                status = True
        except:
            pass
        else:
            status = True

        self._checked[url] = status
        return status

    def process(self, obj):
        urls = []
        for url_tag in 'website', 'contact:website', 'url', 'source_ref':
            if url_tag in obj:
                urls.append(obj[url_tag])

        if urls:
            dead_link = False
            for url in urls:
                if not self._check_url(url):
                    dead_link = True
                    break
            if dead_link:
                self._dead_links.append((obj['tag'], obj['id']))

    def finish(self, issues):
        issues.add_issue_type('errors/website/not_available/', _DEAD_LINKS)
        for obj_type, obj_id in self._dead_links:
            issues.add_issue_obj('errors/website/not_available/', obj_type, obj_id)
