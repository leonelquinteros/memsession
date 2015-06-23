MemSession
----------

Django Middleware for session handling on Google App Engine using Memcache backend


Instructions for a working Django project
-----------------------------------------

Clone or download the middleware class into a directory on your application path.
For the purposes of this document, there will be a directory called 'memsession' inside the ROOT path 
with the 'session.py' middleware class file inside of it:

[ROOT]/memsession/session.py  



1- Setup:
---------

settings.py module:

```
MIDDLEWARE_CLASSES = (
    'memsession.session.MemSession',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
)
```

2- Configure:
-------------

Edit the session.py file to change the default values. 
The most important change you'll want to do is to change the HKEY value to make it unique and secret.
Open the session.py file and look for the following section: 

```
##############################
#                            #
#    CONFIGURE FROM HERE     #
#                            #
##############################

# The name for your session's cookie
SESSION_NAME = 'MemSession'

# Make the HKEY unique
HKEY = 'FF&KEKLDkjd-pfjGruUYn%GfsbTRuTEt5454T$315va'

# Global session identifier.
SESSION_ID = 'MemSession'

# Session's cookie duration in seconds.
MAX_AGE = 3600

##############################
#                            #
#    CONFIGURE UNTIL HERE    #
#                            #
##############################
```

All values can be left as they're by default and everything will work, 
but the HKEY value will be needed to ensure the communication between the client is secure.


3- Usage:
---------

views.py module:
    
```
def index(request):
    hello = request.memSession.read('hello')
    if hello == None:
    	request.memSession.write('hello', 'Hello world (from the session)!!')
    	return HttpResponse( 'Hello world!!' )
    else:
    	return HttpResponse( hello )
```
