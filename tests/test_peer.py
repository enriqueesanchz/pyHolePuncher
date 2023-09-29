# test_peer.py

from pytest import mark
from pyHolePuncher.peer import Peer, NatType
from pyHolePuncher.punch import HolePuncher
import requests


def test_peer_init():
    peer = Peer()
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    assert peer.ip is not None
    assert peer.ip == ip
    assert peer.nat is not None
    assert peer.nat in (NatType.EndpointDependent, NatType.EndpointIndependent)

def test_peer_getNatType():
    peer = Peer()
    assert peer.getNatType() is not None
    assert peer.getNatType() in (NatType.EndpointDependent, NatType.EndpointIndependent)

def test_peer_getIp():
    peer = Peer()
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    assert peer.getIp() == ip


def test_peer_addHolePuncher():
    peer = Peer()
    puncher = peer.addHolePuncher()
    assert puncher in peer.hole_punchers
    
    ports = (puncher.getInternalPort(), puncher.getExternalPorts())
    assert ports in peer.ports

def test_peer_addCandidate():
    candidate = ("47.12.14.18", 5555)
    peer = Peer()
    peer.addCandidate(candidate)
    assert candidate in peer.candidates

@mark.notimplemented
def test_peer_connect():
    pass
