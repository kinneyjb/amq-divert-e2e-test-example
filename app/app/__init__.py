from multiprocessing import Queue
from proton import Message
from proton.reactor import Container
from proton.handlers import MessagingHandler


class Server(MessagingHandler):
    def __init__(
            self,
            host,
            subscribe_address,
            publish_address,
            publish_subject
    ):
        super(Server, self).__init__()
        self.container = Container(self)
        self.conn = self.container.connect(host)
        self.receiver = self.container.create_receiver(
            self.conn,
            subscribe_address
        )
        self.publish_subject = publish_subject
        self.sender = self.container.create_sender(self.conn, publish_address)

    def on_message(self, event):
        message = Message()
        # message.subject = self.publish_subject
        message.properties = {
            'subject': self.publish_subject
        }
        self.transform(event, message)
        self.sender.send(message)

    def transform(self, event, message):
        message.body = event.message.body
        message.body += f'\n{self.publish_subject}'

    def on_connection_close(self, endpoint, error):
        if error:
            print("Closed due to %s" % error)
        self.conn.close()

    def run(self):
        self.container.run()


class EventLogger(MessagingHandler):
    def __init__(self, host, subscribe_address, queue: Queue):
        super(Server, self).__init__()
        self.container = Container(self)
        self.conn = self.container.connect(host)
        self.receiver = self.container.create_receiver(
            self.conn,
            subscribe_address
        )
        self.events = queue

    def on_message(self, event):
        message = Message()
        message.subject = self.publish_subject
        self.transform(event, message)
        self.sender.send(message)

    def on_connection_close(self, endpoint, error):
        if error:
            print("Closed due to %s" % error)
        self.conn.close()

    def run(self):
        self.container.run()
