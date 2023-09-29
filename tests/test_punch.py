# test_punch.py

import socket
from pytest import mark
from pyHolePuncher.punch import HolePuncher


def test_punch_init():
    puncher = HolePuncher()
    assert type(puncher.sock) == socket.socket
    assert puncher.port == puncher.getInternalPort()

def test_punch_internal_port():
    puncher = HolePuncher()
    assert puncher.port == puncher.getInternalPort()

@mark.notimplemented
def test_punch_external_port():
    pass

def test_punch_add_dst():
    puncher = HolePuncher()
    dst = ("10.10.10.10", 5555)
    puncher.addDestination(dst)
    assert dst in puncher.destinations

def test_punch_remove_dst():
    puncher = HolePuncher()
    print(puncher.destinations)
    dst = ("10.10.10.10", 5555)
    puncher.addDestination(dst)
    print(puncher.destinations)
    assert dst in puncher.destinations

    puncher.removeDestination(dst)
    print(puncher.destinations)
    assert dst not in puncher.destinations

def test_punch_clean_dst():
    puncher = HolePuncher()
    dst = ("10.10.10.10", 5555)
    puncher.addDestination(dst)
    assert dst in puncher.destinations

    puncher.cleanDestination()
    assert puncher.destinations == []

@mark.notimplemented
def test_punch_punch():
    pass
