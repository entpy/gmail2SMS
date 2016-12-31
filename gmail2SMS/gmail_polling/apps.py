# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import AppConfig
import logging, sys

# Get an instance of a logger
logger = logging.getLogger(__name__)

class GmailPollingConfig(AppConfig):
    name = 'gmail_polling'

    def ready(self):
        logger.info("applicazione avviata, inizio il polling")
        pass # startup code here
