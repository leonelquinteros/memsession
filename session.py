# Core
import hashlib, time

# Google
from google.appengine.api import memcache

# Http Request
from django.http import HttpRequest, HttpResponse

# The name for your session's cookie
SESSION_NAME = 'MemSession'

# Make the HKEY unique
HKEY = 'FFKEKLDkjdpfjGruUYnGfsbTRuTEt5454T$315va'

# Global session identifier. 
SESSION_ID = 'MemSession'

# Session's cookie duration in seconds.
MAX_AGE = 3600 

def start(request, response):
    global SESSION_NAME, SESSION_ID, MAX_AGE
    
    if not SESSION_NAME in request.COOKIES:
        SESSION_ID = initSession(request, response)
    else:
        if not sessionIsValid(request.COOKIES[SESSION_NAME], request.COOKIES[SESSION_NAME + '_v']):
            SESSION_ID = initSession(request, response)
        else:
            SESSION_ID = request.COOKIES[SESSION_NAME]
            
            # Renew cookie's max_age
            response.set_cookie(SESSION_NAME, SESSION_ID, MAX_AGE)
            response.set_cookie(SESSION_NAME + '_v', generateSessionValidator(SESSION_ID), MAX_AGE)
    
    return True


def initSession(request, response):
    global SESSION_NAME, MAX_AGE
    
    sessId = generateSessionId(request)
    response.set_cookie(SESSION_NAME, sessId, MAX_AGE)
    response.set_cookie(SESSION_NAME + '_v', generateSessionValidator(sessId), MAX_AGE)
    
    return sessId


def generateSessionId(request):
    global HKEY
    
    h = hashlib.sha512()
    
    if 'HTTP_USER_AGENT' in request.META:
        h.update(request.META['HTTP_USER_AGENT'])
    
    h.update(HKEY)
    
    if 'REMOTE_ADDR' in request.META:
        h.update(request.META['REMOTE_ADDR'])
    
    h.update(str(time.time()))
    
    if 'REMOTE_HOST' in request.META:
        h.update(request.META['REMOTE_HOST'])
    
    return h.hexdigest()


def generateSessionValidator(sessId):
    global SESSION_NAME, HKEY
    
    h = hashlib.sha512()
    h.update(sessId)
    h.update(SESSION_NAME)
    h.update(HKEY)
    
    return h.hexdigest()


def sessionIsValid(sessId, sessV):
    global SESSION_NAME, HKEY
    
    h = hashlib.sha512()
    h.update(sessId)
    h.update(SESSION_NAME)
    h.update(HKEY)
    
    if h.hexdigest() == sessV:
        return True
    else:
        return False


def read(key):
    global SESSION_NAME, SESSION_ID
    
    return memcache.get(SESSION_NAME + '.' + SESSION_ID + '.' + key)


def write(key, value):
    global SESSION_NAME, SESSION_ID
    
    memcache.set(SESSION_NAME + '.' + SESSION_ID + '.' + key, value, 86400)
    return True

