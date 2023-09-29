import socket
from typing import List

class HolePuncher():
    sock: socket.socket
    port: int
    destinations: List[tuple] = []

    def __init__(self):
        """Init random socket"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(5)
        self.sock.bind(('0.0.0.0', 0))
        
        self.port = self.sock.getsockname()[1]

    def getInternalPort(self) -> int:
        """Get internal sock port"""
        return self.port

    def getExternalPorts(self) -> tuple:
        """Get NAT port translation from stun servers"""
        pass
    
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

    def punch(self):
        """Try to hole punch destination"""
        pass