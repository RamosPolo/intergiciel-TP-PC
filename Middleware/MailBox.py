class MailBox:
    def __init__(self):
        self.box = list()

    def isEmpty(self):
        return not self.box

    def addMessage(self, msg):
        self.box.append(msg)