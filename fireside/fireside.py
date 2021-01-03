import uuid
import time 
import logging
import threading
from pyfiglet import Figlet
from rx import operators as op 
from agents import PowerfulAgent, Message
log = logging.getLogger(__name__)

class Fireside(PowerfulAgent):

    def setup(self, name='', pub_address=None, sub_address=None, mode='client'):
        self.name=name
        if mode=='server':
            self.create_notification_broker(pub_address, sub_address)
        
        self.pub, self.sub = self.create_notification_client(pub_address, sub_address)
        self.sub.observable \
            .pipe(
                op.filter(lambda x: x['topic']!=self.name)
            ).subscribe(lambda x: self.receive(x))

    def receive(self, msg):
        print("{}: {}".format(msg['topic'], msg['payload']))

    def main(self):
        f = Figlet(font='slant')
        print('\n'+f.renderText('Fireside'))
        print("username: {}".format(self.name))

        # use exit event to gracefully exit loop and graceful cleanup
        while not self.exit_event.is_set(): 
            msg = input("{}: ".format(self.name))
            self.pub.send(Message.notification(topic=self.name, payload=msg))

