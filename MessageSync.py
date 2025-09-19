from enum import Enum

class SyncState(Enum):
    SEND = 0
    CONFIRM = 1

class MessageSync:
    def __init__(self, message, source, to, state=SyncState.SEND):
        self.message = message
        self.horloge = 0
        self.source = source
        self.to = to
        self.state = state

    # retourne le message
    def getObject(self):
        return self.message

    # Retourne la valeur de l'horloge
    def getHorloge(self):
        return self.horloge

    def setHorloge(self, estampille):
        self.horloge = estampille

    def getSource(self):
        return self.source

    def getDestinataire(self):
        return self.to

    def getSender(self):
        return self.getSource()

    def changeToConfirm(self):
        self.state = SyncState.CONFIRM

    def changeToSend(self):
        self.state = SyncState.SEND

    def isSend(self):
        return self.state == SyncState.SEND

    def isConfirm(self):
        return self.state == SyncState.CONFIRM