# #zad1

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

#zad 2

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

#zad 3

# import socket
# import threading
# import time

# HOST = "127.0.0.1"
# TCP_PORT = 2913

# # Sekwencja testowa
# SEKWENCJA = [1666, 2666, 3666]

# # Prawidłowe porty UDP kończące się na 666
# PORTY_UDP = [1666, 2666, 3666, 4666, 5666]

# # Zapamiętanie postępu klienta
# postep = {}
# odblokowani = set()

# blokada = threading.Lock()


# def obsluga_udp(port):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind((HOST, port))
#     print(f"UDP nasłuchuje na {HOST}:{port}")

#     while True:
#         dane, adres = sock.recvfrom(1024)
#         tekst = dane.decode(errors="ignore").strip()

#         if tekst != "PING":
#             continue

#         ip_klienta = adres[0]

#         if port in SEKWENCJA:
#             sock.sendto(b"PONG", adres)

#             with blokada:
#                 aktualny = postep.get(ip_klienta, [])

#                 oczekiwany_index = len(aktualny)

#                 if oczekiwany_index < len(SEKWENCJA) and port == SEKWENCJA[oczekiwany_index]:
#                     aktualny.append(port)
#                     postep[ip_klienta] = aktualny

#                     if aktualny == SEKWENCJA:
#                         odblokowani.add(ip_klienta)
#                         print(f"Odblokowano TCP dla {ip_klienta}")
#                 else:
#                     # zła kolejność → reset
#                     if port == SEKWENCJA[0]:
#                         postep[ip_klienta] = [port]
#                     else:
#                         postep[ip_klienta] = []


# def serwer_tcp():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind((HOST, TCP_PORT))
#     sock.listen(1)

#     print(f"TCP ukryta usługa nasłuchuje na {HOST}:{TCP_PORT}")

#     while True:
#         klient, adres = sock.accept()
#         ip_klienta = adres[0]

#         with blokada:
#             czy_odblokowany = ip_klienta in odblokowani

#         if czy_odblokowany:
#             klient.send(b"Congratulations! You found the hidden.")
#             print(f"Klient {adres} dostał dostęp do ukrytej usługi")

#             with blokada:
#                 odblokowani.discard(ip_klienta)
#                 postep[ip_klienta] = []
#         else:
#             print(f"Klient {adres} probowal polaczyc sie bez poprawnej sekwencji")

#         klient.close()


# # Start wątków UDP
# for port in PORTY_UDP:
#     t = threading.Thread(target=obsluga_udp, args=(port,), daemon=True)
#     t.start()

# # Start TCP
# serwer_tcp()

#zad4

# import socket
# import time

# HOST = "127.0.0.1"
# PORT = 5000
# ROZMIAR = 60000

# dane = b"A" * ROZMIAR

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST, PORT))

# start = time.perf_counter()
# sock.sendall(dane)

# odebrane = 0
# while odebrane < ROZMIAR:
#     fragment = sock.recv(65535)
#     if not fragment:
#         break
#     odebrane += len(fragment)

# koniec = time.perf_counter()

# print("TCP czas:", koniec - start, "s")
# sock.close()



import socket
import time

HOST = "127.0.0.1"
PORT = 5000
ROZMIAR = 60000

dane = b"A" * ROZMIAR

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start = time.perf_counter()
sock.sendto(dane, (HOST, PORT))
odpowiedz, _ = sock.recvfrom(65535)
koniec = time.perf_counter()

print("UDP czas:", koniec - start, "s")
sock.close()