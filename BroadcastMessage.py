class BroadcastMessage:
    def __init__(self, object_message, source):
        self.object = object_message
        self.object.setSender(source)
        self.horloge = 0
        self.source = source

    # retourne le message
    def getObject(self):
        return self.object

    # Retourne la valeur de l'horloge
    def getHorloge(self):
        return self.horloge

    def setHorloge(self, estampille):
        self.horloge = estampille

    def getSource(self):
        return self.source