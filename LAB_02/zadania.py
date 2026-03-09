#zad1

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("ntp.task.gda.pl", 13))

# result = sock.recv(1024)
# print(result.decode())

# sock.close()

#zad2

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("212.182.24.27", 2900))
# # sock.connect(("127.0.0.1", 2900)) # bo serwer z plików działa na localhost

# message = input("Podaj wiadomość:")
# sock.send(message.encode())
# result = sock.recv(1024)
# print(result.decode())

# sock.close()

#zad3

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("212.182.24.27", 2900))
# # sock.connect(("127.0.0.1", 2900)) # bo serwer z plików działa na localhost

# while 1:
#     message = input("Podaj wiadomość:")
#     sock.send(message.encode())
#     result = sock.recv(1024)
#     print(result.decode())

#     if message == "stop":
#         break

# sock.close()

#zad4

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("212.182.24.27", 2901))
# # sock.connect(("127.0.0.1", 2901))

# message = input("Podaj wiadomość:")
# sock.send(message.encode())
# result = sock.recv(1024)
# print(result.decode())

# sock.close()

#zad5

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("212.182.24.27", 2901))
# # sock.connect(("127.0.0.1", 2901))

# while 1:
#     message = input("Podaj wiadomość:")
#     sock.send(message.encode())
#     result = sock.recv(1024)
#     print(result.decode())

#     if message == "stop":
#         break

# sock.close()

#zad6

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("212.182.24.27", 2902))
# # sock.connect(("127.0.0.1", 2902))

# a = input("Podaj pierwszą liczbę: ")
# op = input("Podaj operator (+ - * /): ")
# b = input("Podaj drugą liczbę: ")

# message = a + " " + op + " " + b

# sock.send(message.encode())

# result = sock.recv(1024)
# print("Wynik:", result.decode())

# sock.close()

#zad7

# import socket
# import sys

# host = sys.argv[1]
# port = int(sys.argv[2])

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# result = sock.connect_ex((host, port))

# if result == 0:
#     print("Port jest otwarty")
# else:
#     print("Port jest zamknięty")

# try:
#     service = socket.getservbyport(port)
# except OSError:
#     service = "nieznana usługa"

# print("Usługa:", service)

# sock.close()

#zad8

# import socket
# import sys

# host = sys.argv[1]
# start_port = 1
# end_port = 1024

# print(f"Skanuję {host} porty {start_port}-{end_port}...")

# for port in range(start_port, end_port + 1):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.settimeout(0.2)

#     result = s.connect_ex((host, port))

#     try:
#         service = socket.getservbyport(port)
#     except OSError:
#         service = "nieznana usługa"

#     if result == 0:
#         print(f"Port {port} jest otwarty - usługa: {service}")
#     else:
#         print(f"Port {port} jest zamknięty - usługa: {service}")

#     s.close()

# print("Skanowanie zakończone.")

#zad9

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("212.182.24.27", 2906))
# # sock.connect(("127.0.0.1", 2906))

# ip = input("Podaj adres IP: ")
# sock.send(ip.encode())

# result = sock.recv(1024)
# print("Hostname:", result.decode())

# sock.close()

#zad10

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("212.182.24.27", 2907))
# # sock.connect(("127.0.0.1", 2907))

# host = input("Podaj hostname: ")
# sock.send(host.encode())

# result = sock.recv(1024)
# print("Adres IP:", result.decode())

# sock.close()

#zad11

# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("212.182.24.27", 2908))
# # sock.connect(("127.0.0.1", 2908))

# message = input("Podaj wiadomość:")

# if len(message) < 20:
#     message = message.ljust(20)
# elif len(message) > 20:
#     message = message[:20]

# sock.send(message.encode())

# result = sock.recv(20)
# print(result.decode())

# sock.close()

#zad12

import socket

# HOST = "212.182.24.27"
HOST = "127.0.0.1"
PORT = 2908
MAX_PACKET_LENGTH = 20

def sendall_data(sock, data):
    total_sent = 0

    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Połączenie zostało przerwane podczas wysyłania")
        total_sent += sent

def recvall_data(sock, length):
    data = b""
    bytes_received = 0

    while bytes_received < length:
        chunk = sock.recv(length - bytes_received)
        if not chunk:
            raise RuntimeError("Połączenie zostało przerwane podczas odbierania")
        data += chunk
        bytes_received += len(chunk)

    return data

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

message = input("Podaj wiadomość: ")

if len(message) < MAX_PACKET_LENGTH:
    message = message.ljust(MAX_PACKET_LENGTH)
elif len(message) > MAX_PACKET_LENGTH:
    message = message[:MAX_PACKET_LENGTH]

message_bytes = message.encode()

sendall_data(sock, message_bytes)

result = recvall_data(sock, MAX_PACKET_LENGTH)
print("Odebrano:", result.decode())

sock.close()