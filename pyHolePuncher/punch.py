import socket
import time
from typing import List
from pyHolePuncher.stun import stun

class HolePuncher():

    _TIMEOUT: int = 5

    def __init__(self):
        """Init random socket"""
        self.sock: socket.socket = None
        self.port: int = None
        self.destinations: List[tuple] = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(self._TIMEOUT)
        self.sock.bind(('0.0.0.0', 0))
        
        self.port = self.sock.getsockname()[1]

    def getInternalPort(self) -> int:
        """Get internal sock port"""
        return self.port

    def getExternalPorts(self) -> tuple:
        """Get NAT port translation from stun servers"""
        ip_port = stun(self.sock)
        return [x[1] for x in ip_port]
    
    def addDestination(self, dst: tuple) -> List[tuple]:
        """Add destionation to the list"""
        self.destinations.append(dst)
        return self.destinations

    def removeDestination(self, dst: tuple) -> List[tuple]:
        """Remove destination from list"""
        self.destinations.remove(dst)
        return self.destinations

    def cleanDestination(self) -> List[tuple]:
        """Clean destination list"""
        self.destinations.clear()
        return self.destinations

    def punch(self, tries: int = 10) -> tuple:
        """Try to hole punch destination"""
        for _ in range(tries):
            for dst in self.destinations:
                self.sock.sendto(b'', (dst[0], dst[1]))
            time.sleep(1)
        
        try:
            _, addr = self.sock.recvfrom(1024)
            return (self.sock, addr)
        except socket.timeout as e:
            print(e)
            return ()
