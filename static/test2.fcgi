#!/usr/bin/python2.4

import sys ; sys.path.append('..')
from fcgi import WSGIServer

counter = 0

def myapp(environ, start_response):
    global counter
    counter += 1
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello World! (%d)\n' % counter]

WSGIServer(myapp).run()
