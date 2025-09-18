class Message:
    def __init__(self, message):
        self.message = message
        self.sender = None

    def getMsg(self):
        return self.message

    def setSender(self, sender):
        self.sender = sender

    def getSender(self) -> int:
        return self.sender


