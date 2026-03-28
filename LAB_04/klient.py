#zad1

# import socket

# HOST = "127.0.0.1"
# PORT = 5000

# klient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# klient.connect((HOST, PORT))

# klient.send("podaj czas".encode())

# odpowiedz = klient.recv(1024)
# print("Data i czas:", odpowiedz.decode())

# klient.close()

#zad2

# import socket

# HOST = "127.0.0.1"
# PORT = 5000

# klient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# klient.connect((HOST, PORT))

# wiadomosc = input("Podaj wiadomość: ")
# klient.send(wiadomosc.encode())

# odpowiedz = klient.recv(1024)
# print("Odpowiedź serwera:", odpowiedz.decode())

# klient.close()

#zad3

# import socket

# HOST = "127.0.0.1"
# PORT = 5000

# klient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# wiadomosc = input("Podaj wiadomość: ")
# klient.sendto(wiadomosc.encode(), (HOST, PORT))

# odpowiedz, adres = klient.recvfrom(1024)
# print("Odpowiedź serwera:", odpowiedz.decode())

# klient.close()

#zad4

# import socket

# HOST = "127.0.0.1"
# PORT = 5000

# klient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# liczba1 = input("Podaj pierwszą liczbę: ")
# operator = input("Podaj operator (+ - * /): ")
# liczba2 = input("Podaj drugą liczbę: ")

# wiadomosc = liczba1 + " " + operator + " " + liczba2
# klient.sendto(wiadomosc.encode(), (HOST, PORT))

# odpowiedz, adres = klient.recvfrom(1024)
# print("Wynik:", odpowiedz.decode())

# klient.close()

#zad5

# import socket

# HOST = "127.0.0.1"
# PORT = 5000

# klient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ip = input("Podaj adres IP: ")
# klient.sendto(ip.encode(), (HOST, PORT))

# odpowiedz, adres = klient.recvfrom(1024)
# print("Hostname:", odpowiedz.decode())

# klient.close()

#zad6

# import socket

# HOST = "127.0.0.1"
# PORT = 5000

# klient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# hostname = input("Podaj hostname: ")
# klient.sendto(hostname.encode(), (HOST, PORT))

# odpowiedz, adres = klient.recvfrom(1024)
# print("Adres IP:", odpowiedz.decode())

# klient.close()

#zad7

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("127.0.0.1", 2900))

# message = input("Podaj wiadomość: ")
# sock.send(message.encode())

# result = sock.recv(1024)
# print("Odpowiedź:", result.decode())

# sock.close()

#zad8

import socket

HOST = "127.0.0.1"
PORT = 2900
MAKS_DLUGOSC = 20

def recvall(sock, msg_len):
    msg = b""
    bytes_rcvd = 0

    while bytes_rcvd < msg_len:
        chunk = sock.recv(msg_len - bytes_rcvd)

        if chunk == b"":
            break

        bytes_rcvd += len(chunk)
        msg += chunk

    return msg

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

wiadomosc = input("Podaj wiadomość: ")

if len(wiadomosc) < MAKS_DLUGOSC:
    wiadomosc = wiadomosc.ljust(MAKS_DLUGOSC)
elif len(wiadomosc) > MAKS_DLUGOSC:
    wiadomosc = wiadomosc[:MAKS_DLUGOSC]

sock.sendall(wiadomosc.encode())

odpowiedz = recvall(sock, len(wiadomosc.encode()))
print("Odpowiedź:", odpowiedz.decode())

sock.close()