# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from django.apps import AppConfig
from twisted.internet.task import LoopingCall
from crochet import setup
from gmail_polling.polling import GmailPolling
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

setup()
class GmailPollingConfig(AppConfig):
    name = 'gmail_polling'

    def ready(self):
        logger.info("applicazione avviata, inizio il polling")
        GmailPolling_obj = GmailPolling()
        # TWISTED
        # http://crochet.readthedocs.io/en/1.4.0/introduction.html
        # http://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python
        background_loop = LoopingCall(GmailPolling_obj.loop)
        # avvia subito e quindi ogni 2 secondi
        reactor = background_loop.start(2, now=True)
        # callback in caso di errore
        reactor.addErrback(GmailPolling_obj.periodic_task_crashed)

        return True
