from enum import Enum

class SyncState(Enum):
    SEND = 0
    CONFIRM = 1

class MessageSync:
    def __init__(self, message, source, to, state=SyncState.SEND):
        """
        Initialise un message synchronisé.

        :param message: L'objet message transporté (peut être de tout type selon votre usage).
        :param source: Identifiant ou numéro de la source émettrice du message.
        :param to: Identifiant ou numéro du destinataire du message.
        :param state: État initial de synchronisation (par défaut SyncState.SEND).
        """
        self.message = message
        self.horloge = 0
        self.source = source
        self.to = to
        self.state = state

    def getObject(self):
        """
        Retourne l'objet message contenu dans l'instance.

        :return: L'objet message original.
        """
        return self.message

    def getHorloge(self):
        """
        Retourne la valeur de l'horloge logique associée au message.

        :return: Valeur entière de l'horloge.
        """
        return self.horloge

    def setHorloge(self, estampille):
        """
        Met à jour l'horloge logique du message.

        :param estampille: Nouvelle valeur entière de l'horloge.
        """
        self.horloge = estampille

    def getSource(self):
        """
        Retourne l'identifiant de la source du message.

        :return: Identifiant ou numéro de la source.
        """
        return self.source

    def getDestinataire(self):
        """
        Retourne l'identifiant du destinataire du message.

        :return: Identifiant ou numéro du destinataire.
        """
        return self.to

    def getSender(self):
        """
        Retourne l'identifiant de l'expéditeur du message.
        Équivalent à getSource().

        :return: Identifiant ou numéro de l'expéditeur.
        """
        return self.getSource()

    def changeToConfirm(self):
        """
        Change l'état du message en mode CONFIRM.
        """
        self.state = SyncState.CONFIRM

    def changeToSend(self):
        """
        Change l'état du message en mode SEND.
        """
        self.state = SyncState.SEND

    def isSend(self):
        """
        Vérifie si l'état du message est SEND.
        :return: True si l'état est SyncState.SEND, sinon False.
        """
        return self.state == SyncState.SEND

    def isConfirm(self):
        """
        Vérifie si l'état du message est CONFIRM.
        :return: True si l'état est SyncState.CONFIRM, sinon False.
        """
        return self.state == SyncState.CONFIRM
