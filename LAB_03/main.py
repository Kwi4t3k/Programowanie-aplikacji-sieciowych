import binascii
import socket

def zad13():
    hex_data = """
        ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61
        6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f
        6e 20 69 73 20 66 75 6e"""
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 2910
    clean_data = hex_data.replace(" ", "").replace("\n", "").strip()

    src_port = int(clean_data[0:4], 16)
    dst_port = int(clean_data[4:8], 16)
    payload_hex = clean_data[16:]
    payload_bytes = bytes.fromhex(payload_hex)
    data_str = payload_bytes.decode('ascii')

    message = f"zad14odp;src;{src_port};dst;{dst_port};data;{data_str}"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    try:
        sock.sendto(message.encode('ascii'), (SERVER_IP, SERVER_PORT))
        response, _ = sock.recvfrom(1024)
        print(f"response: {response.decode('ascii')}")
    except Exception as e:
        print(f"error: {e}")
    finally:
        sock.close()

def zad14():
    hex_data = """  
        0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18
        00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee
        00 1a 4c ee 68 65 6c 6c 6f 20 3a 29"""

    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 2909

    clean_data = "".join(hex_data.split())

    src_port = int(clean_data[0:4], 16)
    dst_port = int(clean_data[4:8], 16)

    payload_hex = clean_data[64:]
    payload_bytes = bytes.fromhex(payload_hex)
    data_str = payload_bytes.decode('ascii')

    message = f"zad13odp;src;{src_port};dst;{dst_port};data;{data_str}"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    try:
        sock.sendto(message.encode('ascii'), (SERVER_IP, SERVER_PORT))
        response, _ = sock.recvfrom(1024)
        print(f"response: {response.decode('ascii')}")
    except Exception as e:
        print(f"error: {e}")
    finally:
        sock.close()

def zad15():
    hex_data = """
        45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b
        c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1
        80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01
        00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67
        72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e
        """

    data_hex = "".join(hex_data.split())
    b = bytes.fromhex(data_hex)

    version = (b[0] >> 4)
    ip_header_len = (b[0] & 0x0F) * 4

    src_ip = ".".join(map(str, b[12:16]))
    dst_ip = ".".join(map(str, b[16:20]))
    protocol_type = b[9]  # 6 dla TCP

    tcp_start = ip_header_len
    src_port = int.from_bytes(b[tcp_start:tcp_start + 2], "big")
    dst_port = int.from_bytes(b[tcp_start + 2:tcp_start + 4], "big")

    tcp_header_len = (b[tcp_start + 12] >> 4) * 4

    payload_start = ip_header_len + tcp_header_len
    payload = b[payload_start:].decode('ascii')

    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 2911
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    try:
        msg_a = f"zad15odpA;ver;{version};srcip;{src_ip};dstip;{dst_ip};type;{protocol_type}"
        print(f"Wysyłam A: {msg_a}")
        sock.sendto(msg_a.encode('ascii'), (SERVER_IP, SERVER_PORT))

        resp_a, _ = sock.recvfrom(1024)
        resp_a_txt = resp_a.decode('ascii')
        print(f"Serwer A: {resp_a_txt}")

        if "TAK" in resp_a_txt:
            msg_b = f"zad15odpB;srcport;{src_port};dstport;{dst_port};data;{payload}"
            print(f"Wysyłam B: {msg_b}")
            sock.sendto(msg_b.encode('ascii'), (SERVER_IP, SERVER_PORT))

            resp_b, _ = sock.recvfrom(1024)
            print(f"Serwer B: {resp_b.decode('ascii')}")

    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    zad15()
