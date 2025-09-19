class TokenMessage:
    def __init__(self, source, dest):
        self.name = "token"
        self.dest = dest
        self.source = source

    def getSource(self):
        return self.source

    def getDest(self):
        return self.dest