class Message:
    def __init__(self, message):
        self.message = message
        self.sender = None
        self.destinataire = None

    def getMsg(self):
        return self.message

    def setSender(self, sender):
        self.sender = sender

    def getSender(self):
        return self.sender

    def setDestinataire(self, receiver):
        self.receiver = receiver

    def getDestinataire(self):
        return self.receiver

