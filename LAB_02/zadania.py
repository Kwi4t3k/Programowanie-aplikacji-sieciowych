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

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("212.182.24.27", 2902))
sock.connect(("127.0.0.1", 2901))

a = input("Podaj pierwszą liczbę: ")
op = input("Podaj operator (+ - * /): ")
b = input("Podaj drugą liczbę: ")

message = a + " " + op + " " + b

sock.send(message.encode())

result = sock.recv(1024)
print("Wynik:", result.decode())

sock.close()