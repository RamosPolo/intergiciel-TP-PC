class TokenMessage:
    def __init__(self, source, dest):
        self.name = "token"
        self.dest = dest
        self.source = source

    def getSource(self)->int:
        """
        Retourne la source du message
        :return:
        """
        return self.source

    def getDest(self)->int:
        """
        Retourne le destinataire du message
        :return:
        """
        return self.dest