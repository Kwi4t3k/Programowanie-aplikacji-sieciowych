#!/usr/bin/env python

import socket
import sys
from time import gmtime, strftime


def sprawdz_skladnie(txt):
    pola = txt.split(";")

    if len(pola) != 7:
        return "BAD_SYNTAX"

    if pola[0] != "zad13odp" or pola[1] != "src" or pola[3] != "dst" or pola[5] != "data":
        return "BAD_SYNTAX"

    try:
        src_port = int(pola[2])
        dst_port = int(pola[4])
        data_len = int(pola[6])
    except ValueError:
        return "BAD_SYNTAX"

    if src_port == 60788 and dst_port == 2901 and data_len == 28:
        return "TAK"
    else:
        return "NIE"


HOST = "127.0.0.1"
PORT = 2910

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind((HOST, PORT))
except socket.error as msg:
    print("Bind failed. Message: " + str(msg))
    sys.exit()

print("[%s] UDP Server is waiting for incoming connections ... " %
      strftime("%Y-%m-%d %H:%M:%S", gmtime()))

try:
    while True:
        data, address = sock.recvfrom(1024)
        tekst = data.decode()

        print("[%s] Received %s bytes from client %s. Data: %s" %
              (strftime("%Y-%m-%d %H:%M:%S", gmtime()), len(data), address, tekst))

        if data:
            answer = sprawdz_skladnie(tekst)
            sent = sock.sendto(answer.encode(), address)

            print("[%s] Sent %s bytes back to client %s." %
                  (strftime("%Y-%m-%d %H:%M:%S", gmtime()), sent, address))
finally:
    sock.close()