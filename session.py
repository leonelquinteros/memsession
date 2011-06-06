# Core
import hashlib, time

# Google
from google.appengine.api import memcache

# Http Request
from django.http import HttpRequest, HttpResponse

##############################
#                            #
#    CONFIGURE FROM HERE     #
#                            #
##############################

# The name for your session's cookie
SESSION_NAME = 'MemSession'

# Make the HKEY unique
HKEY = 'FFKEKLDkjdpfjGruUYnGfsbTRuTEt5454T$315va'

# Global session identifier. 
SESSION_ID = 'MemSession'

# Session's cookie duration in seconds.
MAX_AGE = 3600 

##############################
#                            #
#    CONFIGURE UNTIL HERE    #
#                            #
##############################

class MemSession(object):
    _name = ''
    _hkey = ''
    _id = ''
    _maxAge = 3600
    
    
    def __init__(self):
        global SESSION_NAME, HKEY, SESSION_ID, MAX_AGE
        
        self._name = SESSION_NAME
        self._hkey = HKEY
        self._id = SESSION_ID
        self._maxAge = MAX_AGE


    def process_request(self, request):
        self.start(request)
        request.memSession = self
        
        return None

    
    def process_response(self, request, response):
        self.start(request)
        
        # Renew cookie's max_age
        response.set_cookie(self._name, self._id, self._maxAge)
        response.set_cookie(self._name + '_v', self.generateSessionValidator(self._id), self._maxAge)
        
        return response
    
    
    def start(self, request):
        if not self._name in request.COOKIES:
            self._id = self.generateSessionId(request)
        else:
            if not self.sessionIsValid(request.COOKIES[self._name], request.COOKIES[self._name + '_v']):
                self._id = self.generateSessionId(request)
            else:
                self._id = request.COOKIES[self._name]
        
        return self._id
    
    
    def generateSessionId(self, request):
        h = hashlib.sha512()
        
        if 'HTTP_USER_AGENT' in request.META:
            h.update(request.META['HTTP_USER_AGENT'])
        
        h.update(self._hkey)
        
        if 'REMOTE_ADDR' in request.META:
            h.update(request.META['REMOTE_ADDR'])
        
        h.update(str(time.time()))
        
        if 'REMOTE_HOST' in request.META:
            h.update(request.META['REMOTE_HOST'])
        
        return h.hexdigest()
    
    
    def generateSessionValidator(self, sessId):
        h = hashlib.sha512()
        h.update(sessId)
        h.update(self._name)
        h.update(self._hkey)
        
        return h.hexdigest()
    
    
    def sessionIsValid(self, sessId, sessV):
        h = hashlib.sha512()
        h.update(sessId)
        h.update(self._name)
        h.update(self._hkey)
        
        if h.hexdigest() == sessV:
            return True
        else:
            return False
    
    
    def read(self, key):
        return memcache.get(self._name + '.' + self._id + '.' + key)
    
    
    def write(self, key, value):
        memcache.set(self._name + '.' + self._id + '.' + key, value, (self._maxAge * 20))
        return True

