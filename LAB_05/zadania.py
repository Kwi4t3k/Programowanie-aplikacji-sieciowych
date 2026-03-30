# zad1

# import socket

# HOST = "127.0.0.1"
# PORT = 2912

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST, PORT))

# while True:
#     user_input = input("Zakończ działanie programu za pomocą q lub podaj liczbę: ")

#     if user_input.lower() == 'q':
#         break

#     sock.send(user_input.encode())

#     odpowiedz = sock.recv(1024).decode()
#     print("Odpowiedź serwera:", odpowiedz)

#     if "correct" in odpowiedz.lower() or "poprawna" in odpowiedz.lower() or "brawo" in odpowiedz.lower():
#         break

# sock.close()

#zad 2

# import socket
# import random

# HOST = "127.0.0.1"
# PORT = 2912

# wylosowana_liczba = random.randint(1, 100)
# print("Wylosowana liczba:", wylosowana_liczba)

# serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serwer.bind((HOST, PORT))
# serwer.listen(1)

# print("Uruchomiono serwer...")

# klient, adres = serwer.accept()
# print("Połączono")

# while True:
#     dane = klient.recv(1024)

#     if not dane:
#         break

#     tekst = dane.decode().strip()

#     try:
#         liczba = int(tekst)
#     except ValueError:
#         klient.send("Proszę podać liczbę".encode())
#         continue

#     if liczba < wylosowana_liczba:
#         klient.send("Za mała".encode())
#     elif liczba > wylosowana_liczba:
#         klient.send("Za duża".encode())
#     else:
#         klient.send("Brawo, odgadnięto liczbę".encode())
#         break

# klient.close()
# serwer.close()

#zad 3

# import socket
# import time

# HOST = "127.0.0.1"
# TCP_PORT = 2913

# znalezione_porty = []

# for port in range(666, 65536, 1000):
#     udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp.settimeout(0.5)

#     try:
#         udp.sendto(b"PING", (HOST, port))
#         dane, _ = udp.recvfrom(1024)

#         if dane.decode().strip() == "PONG":
#             print("Znaleziono port sekwencji:", port)
#             znalezione_porty.append(port)

#     except:
#         pass

#     udp.close()
#     time.sleep(0.05)

# print("Znalezione porty:", znalezione_porty)

# tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp.settimeout(2)

# try:
#     tcp.connect((HOST, TCP_PORT))
#     odpowiedz = tcp.recv(1024).decode()
#     print("Ukryta usługa odpowiedziała:", odpowiedz)
# except Exception as e:
#     print("Nie udało się połączyć z ukrytą usługą:", e)

# tcp.close()

#zad4

# import socket
# import time

# HOST = "127.0.0.1"
# PORT = 5000

# serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serwer.bind((HOST, PORT))
# serwer.listen(1)

# print("Uruchomiono serwer TCP")

# klient, adres = serwer.accept()

# while True:
#     dane = klient.recv(65535)
#     if not dane:
#         break
#     klient.sendall(dane)

# klient.close()
# serwer.close()




import socket

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer UDP")

while True:
    dane, adres = serwer.recvfrom(65535)
    serwer.sendto(dane, adres)