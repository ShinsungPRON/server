from server.term_colors import *
import configparser
import threading
import socket
import json
import time
import sys
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "controller.conf"))


class ClientSocketHandler(threading.Thread):
    def __init__(self, soc, addr):
        super().__init__()
        self.soc = soc
        self.addr = addr
        print(INFO, f"Handler {self} created for {addr}")

    def run(self):
        while True:
            time.sleep(0.1)

    def send(self, data):
        self.soc.send(data.encode())


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(("localhost", int(config['DEFAULT']['port'])))
soc.listen(10)
connected_client = {}

print(INFO, f"Server listening on (localhost, {config['DEFAULT']['port']})")


def establish_connection():
    print(INFO, "Thread created for establish_connection")
    while True:
        s, a = soc.accept()
        print("\r" + NEW, f"Connection established with {a}")
        client_name = s.recv(1024).decode()
        print(NEW, f"Client name is {client_name}")

        worker = ClientSocketHandler(s, a)
        worker.daemon = True
        worker.start()
        connected_client[client_name] = worker


t = threading.Thread(target=establish_connection)
t.daemon = True
t.start()
time.sleep(0.3)

while True:
    cmd = input("> ").strip()

    if not cmd:
        continue

    if cmd.startswith("."):
        if cmd == '.stop':
            for n, k in connected_client.items():
                k.soc.close()
            print(INFO, "Closing")
            sys.exit()

        elif cmd == ".show":
            for client, thread in connected_client.items():
                print(client, thread.addr)

    else:
        cmd = cmd.split(" ")

        try:
            to = cmd[0]
            action = cmd[1]
            arg = cmd[2]
        except IndexError:
            print(ERROR, "Illegal command")
            continue

        if to not in connected_client.keys() and not to == "broadcast":
            print(ERROR, "Unknown client name:", to)
            continue

        if action == "enable":
            if to == "broadcast":
                for client, thread in connected_client.items():
                    thread.send(json.dumps({
                        "action": "enable",
                        "args": "gacha"
                    }))
                    print(OK, f"command sent to {client}")
            else:
                thread = connected_client[to]
                thread.send(json.dumps({
                    "action": "enable",
                    "args": "gacha"
                }))
                print(OK, f"command sent to {to}")

        elif action == "disable":
            if to == "broadcast":
                for client, thread in connected_client.items():
                    thread.send(json.dumps({
                        "action": "disable",
                        "args": "gacha"
                    }))
                    print(OK, f"command sent to {client}")
            else:
                thread = connected_client[to]
                thread.send(json.dumps({
                    "action": "disable",
                    "args": "gacha"
                }))
                print(OK, f"command sent to {to}")

        else:
            print(ERROR, "Illegal command")

