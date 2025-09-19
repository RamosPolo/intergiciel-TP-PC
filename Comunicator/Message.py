class Message:
    def __init__(self, message):
        self.message = message
        self.sender = None
        self.destinataire = None

    def getMsg(self)->str:
        """
        Retourne l'intitulé du message
        :return: le message
        """
        return self.message

    def setSender(self, sender: int):
        """
        Met à jour la source du message
        :param sender: source du message
        :return:
        """
        self.sender = sender

    def getSender(self)->int:
        """
        Retourne la source du message
        :return: source du message
        """
        return self.sender

    def setDestinataire(self, receiver: int):
        """
        Change le destinataire du message
        :param receiver: nouveau destinataire
        :return:
        """
        self.receiver = receiver

    def getDestinataire(self)->int:
        """
        Retourne le destinataire du message
        :return:
        """
        return self.receiver

