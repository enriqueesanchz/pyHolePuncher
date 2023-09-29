# test_peer.py

from pytest import mark
from pyHolePuncher.user import User, NatType
import requests


def test_user_init():
    user = User()
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    assert user.ip is not None
    assert user.ip == ip
    assert user.nat is not None
    assert user.nat in (NatType.EndpointDependent, NatType.EndpointIndependent)

def test_user_getNatType():
    user = User()
    assert user.getNatType() is not None
    assert user.getNatType() in (NatType.EndpointDependent, NatType.EndpointIndependent)

def test_user_getIp():
    user = User()
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    assert user.getIp() == ip


def test_user_addHolePuncher():
    user = User()
    puncher = user.addHolePuncher()
    assert puncher in user.hole_punchers
    
    ports = (puncher.getInternalPort(), puncher.getExternalPorts())
    assert ports in user.ports

def test_user_addCandidate():
    candidate = ("47.12.14.18", 5555)
    peer = User()
    peer.addCandidate(candidate)
    assert candidate in peer.candidates

@mark.notimplemented
def test_user_connect():
    pass
