# -*- coding: utf-8 -*-

from gmail_polling import gmail
from gmail2SMS import local_settings
from datetime import date
import datetime
import logging, json, nexmo

# Get an instance of a logger
logger = logging.getLogger(__name__)

class GmailPolling():

    # https://github.com/charlierguo/gmail
    gmail_imap = gmail.login(local_settings.c1, local_settings.c2)

    def __init__(self):
        return None

    def loop(self):
        logger.info("controllo la mail in data: " + str(date.today()))
        self.get_unread_email()
        return True

    def get_unread_email(self):
        """List of unread email"""
        emails = self.gmail_imap.inbox().mail(on=date.today(), unread=True, sender=local_settings.sender)
        for email in emails:
            email.fetch()
            email.read()
            # invio l'sms
            print ("invio sms: " + str(email.subject))
            self.send_sms(text=email.subject)

        # fix per far riscaricare i messaggi della inbox, la libreria cachava tutto e se
        # arrivava un nuovo messaggio non veniva tirato giù, ho solo resettato alcuni campi
        self.gmail_imap.mailboxes = {}
        self.gmail_imap.current_mailbox = None
        self.gmail_imap.fetch_mailboxes()

        return True

    def send_sms(self, text):
        """Function to send an sms"""
        client = nexmo.Client(key=local_settings.nexmo_key, secret=local_settings.nexmo_secret)
        for sms_number in local_settings.notify_numbers:
            # se c'è un allarme o è stato disattivato
            if text.find("Allarme") > -1 or text.find("Fin.All.") > -1:
                print("invio a: " + str(sms_number))
                response = client.send_message({'from': local_settings.from_name, 'to': "+39" + str(sms_number), 'text': text})
                response = response['messages'][0]

                if response['status'] == '0':
                  print 'Sent message', response['message-id']

                  print 'Remaining balance is', response['remaining-balance']
                else:
                  print 'Error:', response['error-text']
