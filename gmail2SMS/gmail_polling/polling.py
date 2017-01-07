# -*- coding: utf-8 -*-

from gmail_polling import gmail
from gmail2SMS import local_settings
from datetime import date
import datetime, logging, json, nexmo, time

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
        # prelevo l'elenco di email in base a determinati criteri
        emails = self.gmail_imap.inbox().mail(on=date.today(), unread=True, sender=local_settings.sender)
        for email in emails:
            # prelevo i dati per ogni singola email (oggetto, testo, ...)
            email.fetch()
            # email subject
            email_subject = email.subject
            # se c'è un allarme o un allarme è stato disattivato
            if email_subject.find("Allarme") > -1 or email_subject.find("Fin.All.") > -1:
                # marco la mail come letta
                email.read()
                # invio l'sms
                self.send_sms(text=email_subject)

        # fix per far riscaricare i messaggi della inbox, la libreria cachava tutto e se
        # arrivava un nuovo messaggio non veniva tirato giù, ho solo resettato alcuni campi
        self.gmail_imap.mailboxes = {}
        self.gmail_imap.current_mailbox = None
        self.gmail_imap.fetch_mailboxes()

        return True

    def send_sms(self, text):
        """Function to send an sms"""
        client = nexmo.Client(key=local_settings.nexmo_key, secret=local_settings.nexmo_secret)
        # invio l'sms ad ogni numero telefonico
        for sms_number in local_settings.notify_numbers:
            logger.info("invio a: " + str(sms_number) + " -> testo: " + str(text))
            response = client.send_message({'from': local_settings.from_name, 'to': "+39" + str(sms_number), 'text': text})
            response = response['messages'][0]
            if response['status'] == '0':
              logger.info('Sent message ', response['message-id'])
              logger.info('Remaining balance is ', response['remaining-balance'])
            else:
              logger.error('SMS sending error: ', response['error-text'])

        return True

    def periodic_task_crashed(self, exception):
        """Loop error"""
        logger.error("Errore nel loop (fermare l'app, rilanciarla e capire il misfatto): " + str(exception))

        return True
