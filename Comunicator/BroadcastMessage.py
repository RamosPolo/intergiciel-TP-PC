class BroadcastMessage:
    def __init__(self, object_message, source):
        self.object = object_message
        self.horloge = 0
        self.source = source

    def getObject(self)->object:
        """
        Retourne l'objet du message
        :return: Message
        """
        return self.object

    def getHorloge(self)->int:
        """
        Retourne l'horloge du message
        :return: la valeur de l'horloge
        """
        return self.horloge

    def setHorloge(self, estampille: int)->None:
        """
        Met à jour l'horloge
        :param estampille: nouvelle valeur de l'horloge
        :return:
        """
        self.horloge = estampille

    def getSource(self)->int:
        """
        Retourne la source du message
        :return:
        """
        return self.source

    def getSender(self)->int:
        """
        retourne la source du message
        :return:
        """
        return self.getSource()