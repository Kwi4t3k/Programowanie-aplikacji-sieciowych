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

#zad6

# import socket

# HOST = "127.0.0.1"
# PORT = 5000

# serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serwer.bind((HOST, PORT))

# print("Uruchomiono serwer...")

# while True:
#     dane, adres = serwer.recvfrom(1024)
#     hostname = dane.decode().strip()

#     print("Odebrano od", adres, "hostname:", hostname)

#     try:
#         ip = socket.gethostbyname(hostname)
#     except socket.gaierror:
#         ip = "Nie znaleziono IP"

#     serwer.sendto(ip.encode(), adres)

#zad7

# import socket, select
# from time import gmtime, strftime

# HOST = '127.0.0.1'
# PORT = 2900

# connected_clients_sockets = []

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind((HOST, PORT))
# server_socket.listen(10)

# connected_clients_sockets.append(server_socket)

# print("[%s] TCP ECHO Server is waiting for incoming connections on port %s ... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), PORT))

# while True:

#     read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

#     for sock in read_sockets:

#         if sock == server_socket:

#             sockfd, client_address = server_socket.accept()
#             connected_clients_sockets.append(sockfd)

#             print("[%s] Client %s connected ... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))

#         else:
#             try:
#                 data = sock.recv(4096)
#                 if data:
#                     message = data.decode()

#                     if len(message) > 20:
#                         message = message[:20]

#                     sock.send(message.encode())

#                     print("[%s] Sending back to client %s data: ['%s']... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address, message))
#                 else:
#                     print("[%s] Client (%s) is offline" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))
#                     sock.close()
#                     connected_clients_sockets.remove(sock)
#                     continue

#             except:
#                 print("[%s] Client (%s) is offline" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))
#                 sock.close()
#                 connected_clients_sockets.remove(sock)
#                 continue

# server_socket.close()

#zad8

import socket
import sys

def recvall(sock, msgLen):
    msg = ""
    bytesRcvd = 0

    while bytesRcvd < msgLen:

        chunk = sock.recv(msgLen - bytesRcvd)

        if chunk == "": break

        bytesRcvd += len(chunk)
        msg += chunk

    return msg


remoteServerIP = "127.0.0.1"
port = 2900

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((remoteServerIP, port))

    if result == 0:
        sock.sendall('Just a text \n')
        data = recvall(sock, 4096)

        print("Port {} is open, data = {}".format(port, data.decode(errors="ignore")))
    else:
        print("Port {} is closed".format(port))

    sock.close()

except KeyboardInterrupt:
    print("You pressed Ctrl+C")
    sys.exit()

except socket.gaierror:
    print("Hostname could not be resolved. Exiting")
    sys.exit()

except socket.error:
    print("Couldn't connect to server")
    sys.exit()