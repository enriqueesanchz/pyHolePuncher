from dataclasses import asdict, dataclass
from enum import Enum
import os
from typing import List
from abc import ABC, abstractmethod

import requests


class NatType(int, Enum):
    EndpointIndependent = 1
    EndpointDependent = 2

@dataclass
class Peer():
    username: str
    ip: str
    ports: List[int]
    natType: NatType

@dataclass
class Namespace():
    name: str
    peers: List[Peer]

class Rendezvous(ABC):
    """Abstract class: client for Rendezvous server"""
    
    @abstractmethod
    def getNamespace(self) -> Namespace:
        """Get namespace object from Rendezvous server"""
        pass

    @abstractmethod
    def createNamespace(self) -> Namespace:
        """Create namespace in Rendezvous server"""
        pass
    
    @abstractmethod
    def registerPeer(self) -> Namespace:
        """Register a peer in Rendezvous server"""
        pass
    
    @abstractmethod
    def updatePeer(self) -> Namespace:
        """Update peer info in Rendezvous server"""
        pass

class SimpleHttpRendezvous(Rendezvous):

    _SERVER = os.environ.get("RENDEZVOUS")

    def getNamespace(self, name: str) -> Namespace:
        """Get namespace object from Rendezvous server"""
        response = requests.get(f"{self._SERVER}/namespace/{name}")

        if(response.status_code == 200):
            peers = [Peer(peer["username"], peer["ip"], peer["port"], NatType(peer["natType"])) for peer in response.json()["peers"]]
            namespace = Namespace(response.json["name"], peers)
            return namespace
        else:
            raise NamespaceNotFound

    def createNamespace(self, name: str) -> Namespace:
        """Create namespace in Rendezvous server"""
        namespace = Namespace(name, [])
        response = requests.post(f"{self._SERVER}/namespace/", json=asdict(namespace))

        if(response.status_code == 201):
            return namespace
        elif(response.status_code == 409): #409 -> Namespace already exists
            raise NamespaceExists
        else:
            raise NamespaceNotCreated
    
    def registerPeer(self, name: str, peer: Peer) -> Namespace:
        """Register a peer in Rendezvous server"""
        response = requests.post(f"{self._SERVER}/namespace/{name}", json=asdict(peer))

        if(response.status_code == 201):
            peers = [Peer(peer["username"], peer["ip"], peer["ports"], NatType(peer["natType"])) for peer in response.json()["peers"]]
            namespace = Namespace(response.json["name"], peers)
            return namespace
        elif(response.status_code == 409):
            raise PeerExists
        else:
            raise PeerNotCreated
    
    def updatePeer(self, name: str, peer: Peer) -> Namespace:
        """Update peer info in Rendezvous server"""
        data = {"ip": peer.ip, "ports": peer.ports, "natType": peer.natType}
        response = requests.put(f"{self._SERVER}/namespace/{name}/{peer.username}", json=data)

        if(response.status_code == 200):
            peers = [Peer(peer["username"], peer["ip"], peer["ports"], NatType(peer["natType"])) for peer in response.json()["peers"]]
            namespace = Namespace(response.json["name"], peers)
            return namespace
        else:
            raise PeerNotUpdated


class NamespaceNotFound(Exception):
    pass

class NamespaceNotCreated(Exception):
    pass

class NamespaceExists(Exception):
    pass

class PeerNotCreated(Exception):
    pass

class PeerNotUpdated(Exception):
    pass

class PeerExists(Exception):
    pass
