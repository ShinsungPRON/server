# +-------------+--------------+-----------------------------------------------------------------+
# |   Author    |     Date     |                            Changed                              |
# +-------------+--------------+-----------------------------------------------------------------+
# |   Andrew A  |  2023/10/11  | Initial release                                                 |
# +-------------+--------------+-----------------------------------------------------------------+

import configparser
import socket
import json

config = configparser.ConfigParser()
config.read("conf.conf")

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((config["DEFAULT"]["ServerAddr"], int(config["DEFAULT"]["ServerPort"])))

print(conn.recv(1024).decode())

with open('data.dat', 'r') as f:
    dat = f.read().split("\n")

data = json.dumps(
    {
        "ClientName": config['DEFAULT']['ClientName'],
        "data": {
            "CustomerName": dat[0],
            "ColorCode": dat[1]
        }
    },
    ensure_ascii=False
)

conn.send(data.encode())