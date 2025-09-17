from .MailBox import MailBox
from .Message import Message

class Com:
    def __init__(self):
        self.id = 0
        self.clock = 0
        self.mailbox = MailBox()

    def getMyId(self):
        return self.id

    def getNbProcess(self):
        return 0

    def sendTo(self, message, destinataires):
        return None

    def sendToSync(self, message, destinataires):
        return None

    def synchronize(self):
        return None

    def requestSC(self):
        return None


    def recevFromSync(self, source=int):
        """
        Reçoit le message quand source a fini d'envoyer
        :param source: int
        :return:
        """
        return None

    def broadcast(self, message):
        return None

    def releaseSC(self):
        return None

    def inc_clock(self):
        self.clock += 1

    def put_in_mailbox(self, message):
        self.mailbox.addMessage(message)