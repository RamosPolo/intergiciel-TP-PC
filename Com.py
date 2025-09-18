import threading
from MailBox import MailBox
from Message import Message
from pyeventbus3.pyeventbus3 import *
from BroadcastMessage import BroadcastMessage

class Com:
    def __init__(self, id_in):
        self.myid = id_in
        self.clock = 0
        self.mailbox = MailBox()
        self.estampille = 0
        PyBus.Instance().register(self, self)

    def getMyId(self):
        return self.myid

    def getNbProcess(self):
        return 0

    def sendTo(self, message, destinataires):
        return None

    def sendToSync(self, message, destinataires):
        return None

    def synchronize(self):
        return None

    def requestSC(self):
        return None


    def recevFromSync(self, source=int):
        return None

    def broadcast(self, message):
        self.estampille = self.estampille + 1
        broadcast_message = BroadcastMessage(message, self.myid)
        broadcast_message.setHorloge(self.estampille)

        PyBus.Instance().post(broadcast_message)

        #print("clock sent on message: " + str(broadcast_message.getHorloge()))
        print("<"+str(self.myid)+"> send: " + broadcast_message.getObject().getMsg())

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event):
        if event.getSource() != self.myid:
            # estampillage
            max_estampille = max(self.estampille, event.getHorloge())
            self.estampille = max_estampille + 1
            event.setHorloge(max_estampille + 1)
            # process du message
            #print("clock receive : " + str(max_estampille))
            print(f"{self.myid} reçoit le message : {event.getObject().getMsg()}")
            self.put_in_mailbox(event.getObject())

    def releaseSC(self):
        return None

    def inc_clock(self):
        self.clock += 1

    def put_in_mailbox(self, message):
        self.mailbox.addMessage(message)