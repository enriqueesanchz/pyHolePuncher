#Simple chat app cli

import sys
import threading
from pyHolePuncher.client import Client

def receive(socket):
    """Receive from peer and print into stdout"""
    while True:
        socket.settimeout(None)
        reply = socket.recv(1024)
        if(reply!= b''):
            sys.stdout.write("\b\b\b")
            print(f"{peer_username}: {reply.decode()}\n>> ", end="")


#Only 1 hole puncher: we suppose it's EIM
#We don't support EDM now
client = Client(input("usuario: "))
client.user.addHolePuncher()

while True:
    # Display options to the user
    print("Select an option:")
    print("1. Create a new chat room")
    print("2. Join an existing chat room")
    print("3. Chat to a peer")
    print("4. Exit")

    option = input("Enter the number of the option you want: ")

    if option == "1":
        new_room = input("Enter the name of the new chat room (or '0' to go back): ")
        if new_room == "0":
            continue

        client.createRoom(new_room)


    elif option == "2":
        room = input("Enter the name of the room you want to join (or '0' to go back): ")
        if room == "0":
            continue

        client.joinRoom(room)

    elif option == "3":
        client.update(room)

        for peer in client.rooms[room].peers:
            print("*", peer.username)

        peer_username = input("Enter the username of the peer to chat (or '0' to go back): ")
        if peer_username == "0":
            continue

        if(client.connect(room, peer_username) == True):
            sock = client.user.connected[peer_username][0]
            addr = client.user.connected[peer_username][1]

            #Thread to show peer messages
            t = threading.Thread(target=receive, args=(sock, ))
            t.start()

            while True:
                message = input(">> ")
                # Send the message to the peer
                sock.sendto(message.encode(), addr)

    elif option == "4":
        print("Exiting the application.")
        break

    else:
        print("Invalid option. Please select a valid option.")
