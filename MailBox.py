from Message import Message

class MailBox:
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

    def getMessageFrom(self, from_p=int):
        """
        Retourne le message qui est lui est destiné, et le supprime de la box
        :param from_p: le destinataire du message
        :return:
        """
        for i in range(len(self.box)):
            message = self.box[i]
            print(f"{from_p} cherche le message: {message.getMsg()}, avec dest : {message.getDestinataire()} ")
            #print(f"les dest du message : {message.getDestinataire()}")
            if message.getDestinataire() == from_p:
                return self.box.pop(i)
