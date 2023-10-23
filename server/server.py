from term_colors import *
import configparser
from pprint import pprint
import socket
import threading
import json
import os
import dbhandler

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "serverconf.conf"))
cursor = dbhandler.DBHandler()

def connect(soc):
    try:
        while True:
            msg = soc.recv(1024).decode()
            data = json.loads(msg)
            data['status'] = "waiting"
            data['assignedAt'] = '0'

            pprint(data)
            cursor.insert_data(data)

    except Exception:
        return


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(("localhost", int(config['DEFAULT']['ServerPort'])))
print(INFO, f"Server listening on (localhost, {int(config['DEFAULT']['ServerPort'])})")
soc.listen(10)

while True:
    sock, addr = soc.accept()
    print(INFO_YELLOW, "connection established with", addr)
    threading.Thread(target=connect, args=(sock,)).start()