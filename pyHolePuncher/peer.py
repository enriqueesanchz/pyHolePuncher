from enum import Enum
import socket
from typing import List
from pyHolePuncher.punch import HolePuncher
from pyHolePuncher.stun import stun

class NatType(Enum):
    EndpointIndependent = 1
    EndpointDependent = 2

class Peer():

    def __init__(self):
        """Init peer with IP and NatType set"""
        self.ip: str = self.getIp()
        self.nat: NatType = self.getNatType()
        self.ports: List[tuple] = []
        self.hole_punchers: List[HolePuncher] = []
        self.candidates: List[tuple] = []
        self.connected: List[tuple] = []

    def getNatType(self) -> NatType:
        """Get NatType from stun server"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(10) #TODO: TIMEOUT const
        ip_port = stun(sock)
        sock.close()
        if(len(ip_port) == 1):
            return NatType.EndpointIndependent
        else:
            return NatType.EndpointDependent
        
    def getIp(self) -> str:
        """Get IP from stun server"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(10) #TODO: TIMEOUT const    
        ip_port = stun(sock)
        sock.close()
        return ip_port[0][0]
    
    def addHolePuncher(self) -> HolePuncher:
        """Add hole puncher to list"""
        puncher = HolePuncher()
        self.hole_punchers.append(puncher)
        self.ports.append((puncher.getInternalPort(), puncher.getExternalPorts()))
        return puncher

    def addCandidate(self, candidate: tuple):
        """Add a possible candidate (ip, port) for conexion"""
        self.candidates.append(candidate)

    def connect(self, username: str):
        """Try to connect to other peer"""
        #Get the other peer object from rendezvous
        #Add candidates (ip, port)
        #Start thread trying to connect
            #When succesful add to connected (username, (ip, port))
        pass
