# zad1

# src = input("Podaj nazwę pliku")
# dst = "lab1zad1.txt"
#
# with open(src, "r", encoding="utf-8") as fsrc, open(dst, "w", encoding="utf-8") as fdst:
#     fdst.write(fsrc.read())
#
# print(f"Skopiowano plik {src} do {dst}")

# zad2

# src = input("Podaj nazwę pliku graficznego")
# dst = "lab1zad1.png"
#
# with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
#     fdst.write(fsrc.read())
#
# print(f"Skopiowano obraz {src} do {dst}")

# zad3

# import socket
#
# def check_ipv4(ip: str) -> bool:
#     try:
#         socket.inet_pton(socket.AF_INET, ip)
#         return True
#     except OSError:
#         return False
#
# def check_ipv6(ip: str) -> bool:
#     try:
#         socket.inet_pton(socket.AF_INET6, ip)
#         return True
#     except OSError:
#         return False
#
# ip = input("Podaj adres IP: ")
#
# if check_ipv4(ip):
#     print("Poprawny adres IPv4")
# elif check_ipv6(ip):
#     print("Poprawny adres IPv6")
# else:
#     print("Niepoprawny adres IP")

#zad4

# import socket
# import sys
#
# if len(sys.argv) != 2:
#     sys.exit(1)
#
# ip = sys.argv[1]
#
# try:
#     print(socket.gethostbyaddr(ip)[0])
# except Exception:
#     print("Nie udało się znaleźć hostname dla tego IP")

# zad5

# import socket
# import sys
#
# if len(sys.argv) != 2:
#     sys.exit(1)
#
# hostname = sys.argv[1]
#
# try:
#     print(socket.gethostbyname(hostname))
# except socket.gaierror:
#     print("Nie udało się rozwiązać nazwy hosta na adres IP")

#zad6

# import socket
# import sys
#
# if len(sys.argv) != 3:
#     sys.exit(1)
#
# host = sys.argv[1]
# port = int(sys.argv[2])
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# result = sock.connect_ex((host, port))
#
# if result == 0:
#     print("Połączenie udane")
# else:
#     print("Nie udało się połączyć")
#
# sock.close()

#zad7

import socket
import sys

if len(sys.argv) != 2:
    sys.exit(1)

host = sys.argv[1]
start_port = 1
end_port = 1024

print(f"Skanuję {host} porty {start_port}-{end_port}...")

for port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)

    result = s.connect_ex((host, port))

    if result == 0:
        print("Otwarty port:", port)

    s.close()

print("Skanowanie zakończone.")