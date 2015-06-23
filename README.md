MemSession
----------

Django Middleware for session handling on Google App Engine using Memcache backend


Instructions for a working Django project
-----------------------------------------

Clone or download the middleware class into a directory on your application path.
For the purposes of this document, there will be a directory called 'memsession' inside the ROOT path 
with the 'session.py' middleware class file inside of it:

    [ROOT]/memsession/session.py  



1- SETUP:
---------

settings.py module:
---------------------------------------------------------------

MIDDLEWARE_CLASSES = (
    'memsession.session.MemSession',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

---------------------------------------------------------------



2- USAGE:
---------

views.py module:
---------------------------------------------------------------
    

def index(request):
    hello = request.memSession.read('hello')
    if hello == None:
    	request.memSession.write('hello', 'Hello world (from the session)!!')
    	return HttpResponse( 'Hello world!!' )
    else:
    	return HttpResponse( hello )
    

---------------------------------------------------------------