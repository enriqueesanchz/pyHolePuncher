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

@mark.notwritten
def test_peer_stun():
    pass

def test_peer_addHolePuncher():
    puncher = HolePuncher()
    peer = Peer()
    peer.addHolePuncher(puncher)
    assert puncher in peer.hole_punchers

def test_peer_addCandidate():
    candidate = ("47.12.14.18", 5555)
    peer = Peer()
    peer.addCandidate(candidate)
    assert candidate in peer.candidates

@mark.notimplemented
def test_peer_connect():
    pass
