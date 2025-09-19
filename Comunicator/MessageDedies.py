from .Message import Message

class MessageDedies:
    def __init__(self, message, source, to):
        self.message = message
        self.horloge = 0
        self.source = source
        self.to = to

    # retourne le message
    def getObject(self)->Message:
        """
        Retourne le message
        :return: Message
        """
        return self.message

    # Retourne la valeur de l'horloge
    def getHorloge(self)->int:
        """
        Retourne l'horloge
        :return: l'horloge
        """
        return self.horloge

    def setHorloge(self, estampille: int):
        """
        Met à jour l'horloge
        :param estampille:
        :return:
        """
        self.horloge = estampille

    def getSource(self)->int:
        """
        Retourne la source du message
        :return: la source du message
        """
        return self.source

    def getDestinataire(self)->int:
        """
        Retourne le destinataire du message
        :return:
        """
        return self.to

    def getSender(self)->int:
        """
        Retourne le destinataire du message
        :return:
        """
        return self.getSource()