import socket
from typing import Dict, List
import concurrent.futures
from pyHolePuncher.punch import HolePuncher
from pyHolePuncher.stun import stun
from pyHolePuncher.rendezvous import NatType, Peer


class User():

    _TIMEOUT = 10

    def __init__(self, username):
        """Init user with IP and NatType set"""
        self.username = username
        self.ip: str = self.getIp()
        self.nat: NatType = self.getNatType()
        self.ports: List[tuple] = []
        self.hole_punchers: List[HolePuncher] = []
        self.candidates: List[Peer] = [] #TODO: use ¿?
        self.connected: Dict[str, tuple] = {}
        self.futures: List[concurrent.futures.ThreadPoolExecutor] = []

    def getNatType(self) -> NatType:
        """Get NatType from stun server"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(self._TIMEOUT)
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
        sock.settimeout(self._TIMEOUT)    
        ip_port = stun(sock)
        sock.close()
        return ip_port[0][0]
    
    def addHolePuncher(self) -> HolePuncher:
        """Add hole puncher to list"""
        puncher = HolePuncher()
        self.hole_punchers.append(puncher)
        self.ports.append((puncher.getInternalPort(), puncher.getExternalPorts())) #Future use: analyze patterns
        return puncher

    def addCandidate(self, candidate: Peer):
        """Add a possible candidate (ip, port) for conexion"""
        self.candidates.append(candidate)

    def connect(self, peer: Peer, return_dict=None) -> List[tuple]:
        """Try to connect to other peer"""
        if(peer.natType == NatType.EndpointIndependent):
            #Start thread trying to connect
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for puncher in self.hole_punchers:
                    for port in peer.ports:
                        puncher.addDestination((peer.ip, port))
                    
                    self.futures.append(executor.submit(puncher.punch))

            results = []
            for future in self.futures:
                results.append(future.result())

            #When succesful add to connected (username, (ip, port))
            for connection in results:
                self.connected[peer.username]=connection #TODO: daemon to maintain connections

            if(return_dict != None):
                return_dict[peer.username] = results

            return results
        
        else:
            #TODO: implement connectivity NatType EndpointDependent
            raise NotImplementedError
