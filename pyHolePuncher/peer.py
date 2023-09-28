BIND_REQUEST_MSG = b'\x00\x01'
BIND_RESPONSE_MSG = b'\x01\x01'
STUN_SERVERS=['stun.l.google.com', 'stun1.l.google.com']

from enum import Enum
import secrets
import socket
from typing import List
from pyHolePuncher.punch import HolePuncher

class WrongResponseCode(Exception):
    pass

class NatType(Enum):
    EndpointIndependent = 1
    EndpointDependent = 2

class Peer():
    ip: str
    ports: List[tuple] = []
    nat: NatType
    hole_punchers: List[HolePuncher] = []
    candidates: List[tuple] = []
    connected: List[tuple] = []

    def __init__(self):
        self.ip = self.getIp()
        self.nat = self.getNatType()

    def getNatType(self) -> NatType:
        stun = self.stun(STUN_SERVERS)
        if(len(stun) == 1):
            return NatType.EndpointIndependent
        else:
            return NatType.EndpointDependent
        
    def getIp(self) -> str:
        stun = self.stun(STUN_SERVERS)
        return stun[0][0]

    def stun(self, stun_servers: List[str]):
        """Get ip+port from stun server"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(10) #TODO: TIMEOUT const
        send_data = b''
        msg_len = len(send_data).to_bytes(2, byteorder='big')
        trans_id = secrets.randbits(128).to_bytes(16, byteorder='big')
        data = BIND_REQUEST_MSG+msg_len+trans_id+send_data

        results = {}

        for stun_server in stun_servers:
            sock.sendto(data, (stun_server, 19302))
            recv, _ = sock.recvfrom(2048)
            recvHex = recv.hex()

            if(recv[:2] == BIND_RESPONSE_MSG):
                ip = "{}.{}.{}.{}".format(int(recvHex[-8:-6], 16),int(recvHex[-6:-4], 16),int(recvHex[-4:-2], 16),int(recvHex[-2:], 16))
                port = int(recvHex[-12:-8], 16)
                results[stun_server] = (ip, port)
            else:
                raise WrongResponseCode
        
        resultSet = tuple(set(results.values()))
        return resultSet
    
    def addHolePuncher(self, puncher: HolePuncher):
        self.hole_punchers.append(puncher)
        self.ports.append((puncher.getInternalPort(), puncher.getExternalPorts()))

    def addCandidate(self, candidate: tuple):
        """Add a posible candidate (ip, port) for conexion"""
        self.candidates.append(candidate)

    def connect(self, username: str):
        """Try to connect to other peer"""
        #Get the other peer object from rendezvous
        #Add candidates (ip, port)
        #Start thread trying to connect
            #When succesful add to connected (username, (ip, port))
        pass
