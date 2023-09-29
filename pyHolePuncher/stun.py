import secrets
from typing import List

BIND_REQUEST_MSG = b'\x00\x01'
BIND_RESPONSE_MSG = b'\x01\x01'
STUN_SERVERS=['stun.l.google.com', 'stun1.l.google.com']

class WrongResponseCode(Exception):
    pass

def stun(sock, stun_servers: List[str] = STUN_SERVERS):
    """Get ip+port from stun server"""
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