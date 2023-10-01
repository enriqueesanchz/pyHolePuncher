# test_peer.py

import multiprocessing
from pyHolePuncher.rendezvous import Peer
from pyHolePuncher.user import User, NatType
import requests


def test_user_init():
    user = User("enrique")
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    assert user.ip is not None
    assert user.ip == ip
    assert user.nat is not None
    assert user.nat in (NatType.EndpointDependent, NatType.EndpointIndependent)

def test_user_getNatType():
    user = User("enrique")
    assert user.getNatType() is not None
    assert user.getNatType() in (NatType.EndpointDependent, NatType.EndpointIndependent)

def test_user_getIp():
    user = User("enrique")
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    assert user.getIp() == ip

def test_user_addHolePuncher():
    user = User("enrique")
    puncher = user.addHolePuncher()
    assert puncher in user.hole_punchers
    
    ports = (puncher.getInternalPort(), puncher.getExternalPorts())
    assert ports in user.ports

def test_user_addCandidate():
    candidate = ("47.12.14.18", 5555)
    peer = User("enrique")
    peer.addCandidate(candidate)
    assert candidate in peer.candidates

def test_user_connect():
    """Test connectivity behind nat"""
    enrique = User("enrique")
    enrique.addHolePuncher()
    ports_enrique = [x[0] for x in enrique.ports]

    guille = User("guille")
    guille.addHolePuncher()
    ports_guille = [x[0] for x in guille.ports]

    peer_guille = Peer(guille.username, "127.0.0.1", ports=ports_guille, natType=1) #Fake localhost peers
    peer_enrique = Peer(enrique.username, "127.0.0.1", ports=ports_enrique, natType=1)

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    p = multiprocessing.Process(target=enrique.connect, args=(peer_guille, return_dict))
    jobs.append(p)
    p.start()
    p = multiprocessing.Process(target=guille.connect, args=(peer_enrique, return_dict))
    jobs.append(p)
    p.start()

    for proc in jobs:
        proc.join()

    assert return_dict["enrique"] == [("127.0.0.1", ports_enrique[0])]
    assert return_dict["guille"] == [("127.0.0.1", ports_guille[0])]
