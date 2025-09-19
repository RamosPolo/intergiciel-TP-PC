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