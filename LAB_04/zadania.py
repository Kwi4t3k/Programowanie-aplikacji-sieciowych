#zad1

# import socket
# from datetime import datetime

# HOST = "127.0.0.1"
# PORT = 5000

# serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serwer.bind((HOST, PORT))
# serwer.listen(1)

# print("Uruchomiono serwer...")

# while True:
#     klient, adres = serwer.accept()
#     print("Połączono z:", adres)

#     dane = klient.recv(1024)

#     if dane:
#         teraz = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         klient.send(teraz.encode())

#     klient.close()

#zad2

# import socket
# from datetime import datetime

# HOST = "127.0.0.1"
# PORT = 5000

# serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serwer.bind((HOST, PORT))
# serwer.listen(1)

# print("Uruchomiono serwer...")

# while True:
#     klient, adres = serwer.accept()
#     print("Połączono z:", adres)

#     dane = klient.recv(1024)

#     if(dane):
#         klient.send(dane)

#     klient.close()

#zad3

# import socket
# from datetime import datetime

# HOST = "127.0.0.1"
# PORT = 5000

# serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serwer.bind((HOST, PORT))

# print("Uruchomiono serwer...")

# while True:
#     dane, adres = serwer.recvfrom(1024)
#     print("Odebrano wiadomość od:", adres)

#     if dane:
#         serwer.sendto(dane, adres)

#zad4

# import socket
# from datetime import datetime

# HOST = "127.0.0.1"
# PORT = 5000

# serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serwer.bind((HOST, PORT))

# print("Uruchomiono serwer...")

# while True:
#     dane, adres = serwer.recvfrom(1024)
#     wiadomosc = dane.decode().strip()
#     print("Odebrano wiadomość od:", adres)
#     czesci = wiadomosc.split()

#     if len(czesci) != 3:
#         wynik = "Użyj liczba -> operator -> liczba"
#     else:
#         liczba1, operator, liczba2 = czesci

#         try:
#             liczba1 = float(liczba1)
#             liczba2 = float(liczba2)

#             if operator == "+":
#                 wynik = str(liczba1 + liczba2)
#             elif operator == "-":
#                 wynik = str(liczba1 + liczba2)
#             elif operator == "*":
#                 wynik = str(liczba1 * liczba2)
#             elif operator == "/":
#                 if liczba2 == 0:
#                     wynik = "Nie można dzielić przez zero"
#                 else:
#                     wynik = str(liczba1 / liczba2)
#             else:
#                 wynik = "Nieznany operator"
#         except ValueError:
#             wynik = "Błędne dane"

#     serwer.sendto(wynik.encode(), adres)

#zad5

# import socket

# HOST = "127.0.0.1"
# PORT = 5000

# serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serwer.bind((HOST, PORT))

# print("Uruchomiono serwer...")

# while True:
#     dane, adres = serwer.recvfrom(1024)
#     ip = dane.decode().strip()

#     print("Odebrano od", adres, "IP:", ip)

#     try:
#         hostname = socket.gethostbyaddr(ip)[0]
#     except socket.herror:
#         hostname = "Nie znaleziono hostname"

#     serwer.sendto(hostname.encode(), adres)