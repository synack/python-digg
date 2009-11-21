'''
Loosely based on Mike Verdone's excellent twitter library:
http://github.com/sixohsix/twitter/
'''

from exceptions import Exception
from urllib import urlencode
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

class DiggError(Exception):
    """
    Exception thrown by the Digg object when there is an
    error interacting with digg.com.
    """
    pass

class DiggCall(object):
    def __init__(self, endpoint, methodname='', user_agent=None):
        self.endpoint = endpoint
        self.methodname = methodname
        self.user_agent = user_agent

    def __getattr__(self, k):
        try:
            return object.__getattr__(self, k)
        except AttributeError:
            return DiggCall(self.endpoint, '.'.join((self.methodname, k)).lstrip('.'))

    def __call__(self, **kwargs):
        methodname = self.methodname
        kwargs['method'] = self.methodname
        kwargs['type'] = 'json'

        req = urllib2.Request('%s?%s' % (self.endpoint, urlencode(kwargs)))
        if self.user_agent:
            req.add_header('User-Agent', self.user_agent)
        
        try:
            handle = urllib2.urlopen(req)
            print repr(handle.headers.items())
            return json.loads(handle.read())
        except urllib2.HTTPError, e:
            raise DiggError('Digg sent status %i for method: %s\ndetails: %s' % (e.code, self.methodname, e.fp.read()))

class Digg(DiggCall):
    def __init__(self, endpoint='http://services.digg.com/1.0/endpoint', user_agent='python-digg/0.1'):
        DiggCall.__init__(self, endpoint=endpoint, user_agent=user_agent)

__all__ = ['Digg']
