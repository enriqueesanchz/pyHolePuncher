from typing import Dict
from pyHolePuncher.rendezvous import Namespace, NamespaceExists, NamespaceNotCreated, NamespaceNotFound, Peer, PeerExists, PeerNotCreated, PeerNotUpdated, SimpleHttpRendezvous
from pyHolePuncher.user import User
import logging

class Client():
    
    def __init__(self, username):
        self.user = User(username)
        self.rendezvous = SimpleHttpRendezvous()
        self.rooms: Dict[str, Namespace] = {}

    def createRoom(self, room: str) -> Namespace:
        try:
            namespace = self.rendezvous.createNamespace(room)
            self.rooms[room] = namespace
        except NamespaceExists as e:
            logging.warning(f"La sala {room} ya existe")
            return self.getPeers(room)
        except NamespaceNotCreated as e:
            logging.error(f"[ERROR] No se ha podido crear la sala {room}")
            return None
        
        logging.info(f"Se ha creado la sala {room}")
        return namespace

    def joinRoom(self, room: str) -> Namespace:
        peer_ports = []
        for int_ext in self.user.ports:
            for ext in int_ext[1]:
                peer_ports.append(ext)

        peer = Peer(self.user.username, self.user.ip, peer_ports, self.user.nat)
        
        try:
            namespace = self.rendezvous.registerPeer(room, peer)
            self.rooms[room] = namespace
        except PeerExists as e:
            logging.warning(f"El usuario {self.user.username} ya está en la sala {room}")
            return self.getPeers(room)
        except PeerNotCreated as e:
            logging.error(f"[ERROR] No se ha podido unir a la sala {room}")
            return None
        
        return namespace
        
    def getPeers(self, room: str) -> Namespace:
        try:
            namespace = self.rendezvous.getNamespace(room)
            self.rooms[room] = namespace
        except NamespaceNotFound as e:
            logging.error(f"[ERROR] No se ha encontrado la sala {room}")
            return None
        
        return namespace
    
    def update(self, room: str) -> Namespace:
        try:
            peer_ports = []
            for int_ext in self.user.ports:
                for ext in int_ext[1]:
                    peer_ports.append(ext)

            peer = Peer(self.user.username, self.user.ip, peer_ports, self.user.nat)
            namespace = self.rendezvous.updatePeer(room, peer)
            self.rooms[room] = namespace
            return namespace
        except PeerNotUpdated as e:
            logging.error(f"[ERROR] No se ha podido actualizar el usuario en la sala {room}")
            return None
        
    def connect(self, namespace: str, username: str) -> bool:
        room = self.rooms[namespace]

        for user in room.peers:
            if(user.username == username):
                peer = Peer(user.username, user.ip, user.ports, user.natType)
                ip_port = self.user.connect(peer)
                if(ip_port != []):
                    return True
                else:
                    return False
        
        return False
