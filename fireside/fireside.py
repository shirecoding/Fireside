import logging
import time 
import uuid

from agents import Message
from agents import PowerfulAgent
from clint.textui import colored
from clint.textui import indent
from clint.textui import puts
from pyfiglet import Figlet
from rx import operators as op
log = logging.getLogger(__name__)

class Fireside(PowerfulAgent):

    def setup(self, name='', pub_address='tcp://0.0.0.0:5000', sub_address='tcp://0.0.0.0:5001', mode='client'):
        self.name = name if name else uuid.uuid4()
        if mode == 'server':
            self.create_notification_broker(pub_address, sub_address)
        self.pub_address = pub_address
        self.sub_address = sub_address
        self.pub, self.sub = self.create_notification_client(pub_address, sub_address)
        self.sub.observable \
            .pipe(
                op.filter(lambda x: x['topic']!=self.name)
            ).subscribe(lambda x: self.receive(x))

    def receive(self, msg):
        puts(colored.magenta(msg['topic'] + ': ') + msg['payload'])

    def main(self):
        f = Figlet(font='slant')
        puts('\n'+f.renderText('Fireside'))
        puts('Welcom to Fireside!!!')
        with indent(4, quote=' >'):
            puts(colored.green('username: ') + self.name)
            puts(colored.green('pub_address: ') + self.pub_address)
            puts(colored.green('sub_address: ') + self.sub_address)

        puts('Connect to this Fireside')    
        with indent(4, quote=' >'):
            puts('fireside ', self.pub_address, self.sub_address, '{{username}}')

        # use exit event to gracefully exit loop and graceful cleanup
        while not self.exit_event.is_set(): 
            msg = input(colored.cyan(self.name + ' : '))
            if msg:
                self.pub.send(Message.notification(topic=self.name, payload=msg))

