class MessageSync:
    def __init__(self, message, source, to, etat):
        self.message = message
        self.horloge = 0
        self.source = source
        self.to = to

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