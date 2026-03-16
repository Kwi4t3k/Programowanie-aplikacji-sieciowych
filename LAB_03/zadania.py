#zad13

# import socket

# hex_data = (
#     "ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61 "
#     "6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f "
#     "6e 20 69 73 20 66 75 6e"
# )

# bajty = bytes.fromhex(hex_data)

# port_zrodlowy = int.from_bytes(bajty[0:2], byteorder="big")
# port_docelowy = int.from_bytes(bajty[2:4], byteorder="big")
# dlugosc_udp = int.from_bytes(bajty[4:6], byteorder="big")
# dlugosc_danych = dlugosc_udp - 8

# wiadomosc = f"zad13odp;src;{port_zrodlowy};dst;{port_docelowy};data;{dlugosc_danych}"
# print(wiadomosc)

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("212.182.24.27", 2910))
# # sock.connect(("127.0.0.1", 2910))

# sock.send(wiadomosc.encode())
# odpowiedz = sock.recv(1024)

# print("Odpowiedź serwera:", odpowiedz.decode())
# sock.close()

#zad14

# import socket

# hex_data = (
#     "0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18 "
#     "00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee "
#     "00 1a 4c ee 68 65 6c 6c 6f 20 3a 29"
# )

# bajty = bytes.fromhex(hex_data)

# port_zrodlowy = int.from_bytes(bajty[0:2], byteorder="big")
# port_docelowy = int.from_bytes(bajty[2:4], byteorder="big")

# dlugosc_naglowka = (bajty[12] >> 4) * 4
# dane = bajty[dlugosc_naglowka:].decode()

# wiadomosc = f"zad14odp;src;{port_zrodlowy};dst;{port_docelowy};data;{dane}"
# print(wiadomosc)

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect(("212.182.24.27", 2909))
# # sock.connect(("127.0.0.1", 2910))

# sock.send(wiadomosc.encode())
# odpowiedz = sock.recv(1024)

# print("Odpowiedź serwera:", odpowiedz.decode())
# sock.close()

#zad15

import socket

hex_data = (
    "45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b "
    "c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1 "
    "80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01 "
    "00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67 "
    "72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e"
)

bajty = bytes.fromhex(hex_data)

# --- IP ---
wersja = bajty[0] >> 4
ihl = (bajty[0] & 0x0F) * 4
total_length = int.from_bytes(bajty[2:4], byteorder="big")
typ_protokolu = bajty[9]

src_ip = ".".join(str(b) for b in bajty[12:16])
dst_ip = ".".join(str(b) for b in bajty[16:20])

# --- TCP ---
tcp_start = ihl
src_port = int.from_bytes(bajty[tcp_start:tcp_start+2], byteorder="big")
dst_port = int.from_bytes(bajty[tcp_start+2:tcp_start+4], byteorder="big")

tcp_header_length = (bajty[tcp_start+12] >> 4) * 4
data_start = tcp_start + tcp_header_length
data = bajty[data_start:total_length].decode()

msg_a = f"zad15odpA;ver;{wersja};srcip;{src_ip};dstip;{dst_ip};type;{typ_protokolu}"
msg_b = f"zad15odpB;srcport;{src_port};dstport;{dst_port};data;{data}"

print(msg_a)
print(msg_b)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("212.182.24.27", 2911))
# sock.connect(("127.0.0.1", 2911))

sock.send(msg_a.encode())
odp_a = sock.recv(1024).decode()
print("Odpowiedź A:", odp_a)

if odp_a == "TAK":
    sock.send(msg_b.encode())
    odp_b = sock.recv(1024).decode()
    print("Odpowiedź B:", odp_b)

sock.close()