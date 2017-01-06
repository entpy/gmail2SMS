"""
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
import logging, json
from twisted.internet import task
from twisted.internet import reactor

# Get an instance of a logger
logger = logging.getLogger(__name__)

def www_index(request):
    ""Home page view""
    timeout = 1.0 # ogni secondo
    logger.info("ho chiamato la view")
    l = task.LoopingCall(doWork)
    l.start(timeout) # call every sixty seconds

    reactor.run(installSignalHandlers=0)
    return HttpResponse("Pagina di prova", content_type="text/html")

def www_index_no_loop(request):
    ""Index no loop page""
    return HttpResponse("Pagina di prova senza loop", content_type="text/html")

def doWork():
    #do work here
    logger.info("loop di twisted")
    return True
"""
