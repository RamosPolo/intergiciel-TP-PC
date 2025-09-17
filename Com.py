class Com():
    def __init__(self):
        self.id = 0
        self.clock = 0
        self.mailbox = ""

    def getMyId(self):
        return self.id

    def getNbProcess(self):
        return 0

    def sendTo(self, message, destinataire):
        return None

    def sendToSync(self, message, destinataire):
        return None

    def synchronize(self):
        return None

    def requestSC(self):
        return None

    def recevFromSync(self, message, source):
        return None

    def broadcast(self, message):
        return None

    def releaseSC(self):
        return None