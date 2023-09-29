# test_punch.py

import socket
import concurrent.futures
from pytest import mark
from pyHolePuncher.punch import HolePuncher
from pyHolePuncher.stun import stun


def test_punch_init():
    puncher = HolePuncher()
    assert type(puncher.sock) == socket.socket
    assert puncher.port == puncher.getInternalPort()

def test_punch_internal_port():
    puncher = HolePuncher()
    assert puncher.port == puncher.getInternalPort()

def test_punch_external_port():
    puncher = HolePuncher()
    puncher_ports = puncher.getExternalPorts()

    ip_port = stun(puncher.sock)
    ports = [x[1] for x in ip_port]

    assert ports == puncher_ports

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

def test_punch_punch():
    """Test punch connectivity behind nat"""
    puncher1 = HolePuncher()
    puncher2 = HolePuncher()

    puncher1.addDestination(("127.0.0.1", puncher2.getInternalPort()))
    puncher2.addDestination(("127.0.0.1", puncher1.getInternalPort()))
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(puncher1.punch)
        future2 = executor.submit(puncher2.punch)
        addr1 = future1.result()
        addr2 = future2.result()

    assert addr1 == ("127.0.0.1", puncher2.getInternalPort())
    assert addr2 == ("127.0.0.1", puncher1.getInternalPort())
