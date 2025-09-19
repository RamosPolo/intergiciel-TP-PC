import threading
import queue
import time
from enum import Enum
from MailBox import MailBox
from Message import Message
from pyeventbus3.pyeventbus3 import *
from BroadcastMessage import BroadcastMessage
from MessageDedies import MessageDedies
from TokenMessage import TokenMessage
from MessageSync import MessageSync


# états pour le token
class SCState(Enum):
    NO_TOKEN = 0
    REQUEST = 1
    SC = 2
    RELEASE = 3

class Com:
    def __init__(self, id_in):
        self.myid = id_in
        self.clock = 0
        self.mailbox = MailBox()
        self.mailbox_intern = MailBox()
        self.estampille = 0
        self.nb_process = 3     # TODO : Mettre à jour cette valeur

        self.has_token = (id_in == 0)
        self.state = SCState.NO_TOKEN if not self.has_token else SCState.SC

        # thread pour gérer le token
        self.token_cond = threading.Condition()

        PyBus.Instance().register(self, self)

    def getMyId(self):
        return self.myid

    def getNbProcess(self):
        return self.nb_process

    def sendTo(self, message, to):
        message_c = Message(message)
        message_to_send = MessageDedies(message_c, self.myid, to)
        self.estampille += 1
        message_to_send.setHorloge(self.estampille)
        PyBus.Instance().post(message_to_send)
        print(f"- [sendTo] <{self.getMyId()}> envoie à {to} : {message}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageDedies)
    def onReceive(self, event):
        if event.getDestinataire() == self.myid:
            msg = event.getObject()
            max_estampille = max(self.estampille, event.getHorloge())
            self.estampille = max_estampille + 1
            event.setHorloge(max_estampille + 1)
            print(f"- [onReceive] <{self.getMyId()}> reçoit de {event.getSource()} : {msg.getMsg()}")
            msg.setSender(event.getSender())
            self.put_in_mailbox(msg)

    def sendToSync(self, message, destinataires):
        message_to_send = Message(message)
        message_to_send.setDestinataire(destinataires)
        mess_sync = MessageSync(message_to_send, self.myid, destinataires, "lol")
        self.estampille += 1
        mess_sync.setHorloge(self.estampille)
        print(f"- [sentToSync] <{self.myid}> Envoie : #{message}# à {destinataires}")
        PyBus.Instance().post(mess_sync)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageSync)
    def recevSyncMessages(self, event):
        if event.getDestinataire() == self.myid :
            msg = event.getObject()
            print("put mailbox interne sync")
            self.mailbox_intern.addMessage(msg)

    def recevFromSync(self, source=int):
        msg = None
        while msg is None:
            time.sleep(1)
            msg = self.getMessageFromBox(source)
        print(f"- [recevFromSync] <{self.myid}> reçoit : {msg.getMsg()} de {str(source)}")

    def synchronize(self):
        print("Synchronisation des Processus...")

    def requestSC(self):
        self.state = SCState.REQUEST
        while not (self.state == SCState.SC):
            time.sleep(1)

    def releaseSC(self):
        self.state = SCState.RELEASE

    @subscribe(threadMode=Mode.PARALLEL, onEvent=TokenMessage)
    def onToken(self, event):
        if event.getDest() == self.myid:
            if self.state == SCState.REQUEST:
                self.state = SCState.SC
                while not (self.state == SCState.RELEASE):
                    time.sleep(1)
            # send next
            self.state = SCState.NO_TOKEN
            next_node =  (self.myid + 1) % self.nb_process
            msg = TokenMessage(self.myid, next_node)
            PyBus.Instance().post(msg)

    def broadcast(self, message):
        message_send = Message(message)
        self.estampille = self.estampille + 1
        broadcast_message = BroadcastMessage(message_send, self.myid)
        broadcast_message.setHorloge(self.estampille)
        PyBus.Instance().post(broadcast_message)
        #print("clock sent on message: " + str(broadcast_message.getHorloge()))
        print("- [broadcast] <"+str(self.myid)+"> send: " + message)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event):
        if event.getSource() != self.myid:
            msg = event.getObject()
            # estampillage
            max_estampille = max(self.estampille, event.getHorloge())
            self.estampille = max_estampille + 1
            event.setHorloge(max_estampille + 1)
            #print("clock receive : " + str(max_estampille))
            print(f"- [broadcast] <{self.myid}> reçoit le message : {msg.getMsg()}")
            msg.setSender(event.getSender())
            self.put_in_mailbox(msg)

    def inc_clock(self):
        self.clock += 1

    def put_in_mailbox(self, message):
        self.mailbox.addMessage(message)

    def getMessageFromBox(self, to=int) -> Message | None:
        """
        Retourne le message qui est destiné au to et le supprime de la pile
        :param to: le destinataire du message
        :return:
        """
        return self.mailbox_intern.getMessageFrom(to)
