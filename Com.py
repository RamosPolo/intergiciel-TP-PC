import threading
import queue
import time
from enum import Enum
from MailBox import MailBox
from MailBoxSync import MailBoxSync
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
        self.mailbox_intern = MailBoxSync()
        self.estampille = 0
        self.nb_process = 3     # TODO : Mettre à jour cette valeur

        self.has_token = (id_in == 0)   # TODO : trouver le leader plus tard
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

    def broadcastSync(self, message_obj, from_id):
        if self.myid == from_id:
            # envoie message
            self.estampille += 1
            horloge = self.estampille
            print(f"[broadcastSync] <{self.myid}> envoie à tous : #{message_obj}#")

            # envoyer à chaque destinataire
            for process in range(self.getNbProcess()):
                if process == self.myid:
                    continue
                m = Message(message_obj)
                sync_msg = MessageSync(m, self.myid, process)
                sync_msg.changeToSend()
                sync_msg.setHorloge(horloge)
                PyBus.Instance().post(sync_msg)

            # attendre les confirmations de tous
            confirmations_recues = set()
            while len(confirmations_recues) < self.getNbProcess() - 1:
                time.sleep(0.5)
                # récupérer toutes les confirmations
                conf = self.mailbox_intern.getMessageConfirmationFromAny()
                if conf and conf.getSource() not in confirmations_recues:
                    confirmations_recues.add(conf.getSource())
                    print(f"- [broadcastSync] <{self.myid}> confirmation de {conf.getSource()}")
            print(f"[broadcastSync] <{self.myid}> Tous les processus ont accusé réception.")

        else:
            # on reçoit le message
            msg_sync = None
            while msg_sync is None:
                time.sleep(0.5)
                msg_sync = self.mailbox_intern.getMessageFromSync(from_id)
            # placer le vrai Message dans la mailbox principale
            self.mailbox.addMessage(msg_sync.getObject())
            print(f"[broadcastSync] <{self.myid}> a reçu le broadcast de {from_id}")

            # envoyer la confirmation au processus source
            self.sendConfirmation(msg_sync.getObject(), from_id)
            print(f"[broadcastSync] <{self.myid}> a envoyé la confirmation à {from_id}")


    def sendToSync(self, message, destinataires):
        message_to_send = Message(message)
        message_to_send.setDestinataire(destinataires)

        mess_sync = MessageSync(message_to_send, self.myid, destinataires)
        mess_sync.changeToSend()

        self.estampille += 1
        mess_sync.setHorloge(self.estampille)
        print(f"- [sentToSync] <{self.myid}> Envoie : #{message}# à {destinataires}")
        PyBus.Instance().post(mess_sync)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageSync)
    def recevSyncMessages(self, event):
        if event.getDestinataire() == self.myid:
            self.mailbox_intern.addMessage(event)
            if event.isSend():
                msg = event.getObject()
                print("put mailbox interne sync")
                self.mailbox.addMessage(msg)
                self.sendConfirmation(msg, event.getSource())

    def sendConfirmation(self, message, to):
        message_c = MessageSync(message, self.myid, to)
        message_c.changeToConfirm()
        print(f"<{self.myid}> Envoie de la confirmation à {to}")
        PyBus.Instance().post(message_c)

    def recevFromSync(self, source=int):
        msg = None
        while msg is None:
            time.sleep(1)
            msg = self.mailbox_intern.getMessageFromSync(source)
        print(f"- [recevFromSync] <{self.myid}> reçoit : {msg.getObject().getMsg()} de {str(source)}")

    def recevFromSyncConfirmation(self, source=int):
        msg = None
        while msg is None:
            time.sleep(1)
            msg = self.mailbox_intern.getMessageConfirmationFrom(source)
        print(f"- [recevFromSyncConfirmation] <{self.myid}> reçoit confirmation de {str(source)}")


    def synchronize(self):
        print("Synchronisation des Processus...")
        self.broadcastSync("SYNC", self.myid)

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
