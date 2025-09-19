from Message import Message

class MailBoxSync:
    def __init__(self):
        self.box = list()

    def isEmpty(self):
        return not self.box

    def addMessage(self, msg):
        self.box.append(msg)

    def getMsg(self) -> Message:
        """
        Retourne l'élement qui a été inséré en premier et le supprime de la liste
        :return:
        """
        return self.box.pop(-1)

    def getLastMsg(self) -> Message:
        """
        Retourne le dernier élement inséré
        :return:
        """
        return self.box[0]

    def getMessageConfirmationFrom(self, from_p=int):
        """
        Retourne le message qui est lui est destiné, et le supprime de la box
        :param from_p: le destinataire du message
        :return:
        """
        for i in range(len(self.box)):
            message_sync = self.box[i]
            #print(f"les dest du message : {message.getDestinataire()}")
            if message_sync.isReceive() and message_sync.getSource() == from_p:
                return self.box.pop(i)

    def getMessageFromSync(self, source):
        for i in range(len(self.box)):
            message_sync = self.box[i]
            #print(f"Message courant : {message_sync.getSource()}, est message d'envoie ? : {message_sync.isSend()}")
            if message_sync.isSend() and message_sync.getSource() == source:
                return self.box.pop(i)
