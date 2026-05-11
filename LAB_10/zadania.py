import socket
import base64
import hashlib
import os

# DANE WSPÓLNE
WS_HOST = "localhost"
WS_PORT = 10000
WS_PATH = "/.ws"

LOCAL_WS_HOST = "127.0.0.1"
LOCAL_WS_PORT = 9001

WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

# POMOCNICZE FUNKCJE
def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Połączenie zostało zamknięte")
        data += chunk
    return data


def recv_until(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data


def generate_ws_key():
    return base64.b64encode(os.urandom(16)).decode()


def compute_accept(key):
    raw = (key + WS_GUID).encode()
    sha1 = hashlib.sha1(raw).digest()
    return base64.b64encode(sha1).decode()


def websocket_handshake(host, port, path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    key = generate_ws_key()

    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        f"Origin: http://{host}:{port}\r\n"
        "\r\n"
    )

    sock.sendall(request.encode())
    response = recv_until(sock, b"\r\n\r\n").decode(errors="ignore")

    print("=== REQUEST ===")
    print(request)
    print("=== RESPONSE ===")
    print(response)

    expected_accept = compute_accept(key)

    if "101 Switching Protocols" not in response:
        raise RuntimeError("Handshake nie powiódł się")

    if expected_accept not in response:
        raise RuntimeError("Niepoprawny Sec-WebSocket-Accept")

    return sock


def build_masked_text_frame(text):
    payload = text.encode("utf-8")
    frame = bytearray()
    frame.append(0x81)  # FIN=1, opcode=1 (text)

    payload_len = len(payload)
    mask_bit = 0x80

    if payload_len <= 125:
        frame.append(mask_bit | payload_len)
    elif payload_len <= 65535:
        frame.append(mask_bit | 126)
        frame.extend(payload_len.to_bytes(2, "big"))
    else:
        frame.append(mask_bit | 127)
        frame.extend(payload_len.to_bytes(8, "big"))

    mask_key = os.urandom(4)
    frame.extend(mask_key)

    masked_payload = bytearray()
    for i, b in enumerate(payload):
        masked_payload.append(b ^ mask_key[i % 4])

    frame.extend(masked_payload)
    return bytes(frame)


def build_unmasked_text_frame(text):
    payload = text.encode("utf-8")
    frame = bytearray()
    frame.append(0x81)  # FIN=1, opcode=1

    payload_len = len(payload)

    if payload_len <= 125:
        frame.append(payload_len)
    elif payload_len <= 65535:
        frame.append(126)
        frame.extend(payload_len.to_bytes(2, "big"))
    else:
        frame.append(127)
        frame.extend(payload_len.to_bytes(8, "big"))

    frame.extend(payload)
    return bytes(frame)


def recv_ws_frame(sock):
    first_two = recv_exact(sock, 2)
    b1, b2 = first_two[0], first_two[1]

    fin = (b1 >> 7) & 1
    opcode = b1 & 0x0F
    masked = (b2 >> 7) & 1
    payload_len = b2 & 0x7F

    if payload_len == 126:
        payload_len = int.from_bytes(recv_exact(sock, 2), "big")
    elif payload_len == 127:
        payload_len = int.from_bytes(recv_exact(sock, 8), "big")

    mask_key = b""
    if masked:
        mask_key = recv_exact(sock, 4)

    payload = recv_exact(sock, payload_len)

    if masked:
        unmasked = bytearray()
        for i, b in enumerate(payload):
            unmasked.append(b ^ mask_key[i % 4])
        payload = bytes(unmasked)

    return {
        "fin": fin,
        "opcode": opcode,
        "payload": payload
    }


def close_ws(sock):
    try:
        sock.sendall(bytes([0x88, 0x00]))
    except:
        pass
    sock.close()


# ZADANIE 1
def zadanie_1():
    sock = websocket_handshake(WS_HOST, WS_PORT, WS_PATH)
    print("Handshake zakończony poprawnie.")
    close_ws(sock)


# ZADANIE 2
def zadanie_2():
    sock = websocket_handshake(WS_HOST, WS_PORT, WS_PATH)

    message = input("Podaj krótką wiadomość (<=125 bajtów): ")
    if len(message.encode("utf-8")) > 125:
        print("Wiadomość jest za długa.")
        close_ws(sock)
        return

    frame = build_masked_text_frame(message)
    sock.sendall(frame)

    response = recv_ws_frame(sock)
    print("Odpowiedź serwera:", response["payload"].decode(errors="ignore"))

    close_ws(sock)

# ZADANIE 3
def zadanie_3():
    sock = websocket_handshake(WS_HOST, WS_PORT, WS_PATH)

    message = input("Podaj wiadomość dowolnej długości: ")
    frame = build_masked_text_frame(message)
    sock.sendall(frame)

    response = recv_ws_frame(sock)
    print("Odpowiedź serwera:", response["payload"].decode(errors="ignore"))

    close_ws(sock)

# ZADANIE 4
def uruchom_serwer_websocket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCAL_WS_HOST, LOCAL_WS_PORT))
    server.listen(1)

    print(f"Serwer WebSocket działa na {LOCAL_WS_HOST}:{LOCAL_WS_PORT}")

    while True:
        conn, addr = server.accept()
        print("Połączono z:", addr)

        try:
            request = recv_until(conn, b"\r\n\r\n").decode(errors="ignore")
            print("=== HANDSHAKE REQUEST ===")
            print(request)

            key = None
            for line in request.split("\r\n"):
                if line.lower().startswith("sec-websocket-key:"):
                    key = line.split(":", 1)[1].strip()
                    break

            if not key:
                conn.close()
                continue

            accept = compute_accept(key)

            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept}\r\n"
                "\r\n"
            )

            conn.sendall(response.encode())
            print("=== HANDSHAKE RESPONSE ===")
            print(response)

            while True:
                frame = recv_ws_frame(conn)
                opcode = frame["opcode"]
                payload = frame["payload"]

                if opcode == 0x8:
                    print("Klient zamknął połączenie.")
                    break

                if opcode == 0x1:
                    text = payload.decode(errors="ignore")
                    print("Odebrano:", text)

                    reply = build_unmasked_text_frame(text)
                    conn.sendall(reply)

        except Exception as e:
            print("Błąd:", e)

        conn.close()

# KLIENT TESTOWY DO ZADANIA 4
def klient_testowy_do_zadania_4():
    sock = websocket_handshake(LOCAL_WS_HOST, LOCAL_WS_PORT, "/")

    message = input("Podaj wiadomość do lokalnego serwera: ")
    frame = build_masked_text_frame(message)
    sock.sendall(frame)

    response = recv_ws_frame(sock)
    print("Odpowiedź serwera:", response["payload"].decode(errors="ignore"))

    close_ws(sock)

if __name__ == "__main__":
    print("Wybierz zadanie:")
    print("1 - handshake z lokalnym echo-serverem Docker")
    print("2 - handshake + krótka wiadomość <=125 bajtów")
    print("3 - handshake + wiadomość dowolnej długości")
    print("4 - uruchom lokalny serwer WebSocket")
    print("5 - klient testowy do zadania 4")

    wybor = input("Twój wybór: ").strip()

    if wybor == "1":
        zadanie_1()
    elif wybor == "2":
        zadanie_2()
    elif wybor == "3":
        zadanie_3()
    elif wybor == "4":
        uruchom_serwer_websocket()
    elif wybor == "5":
        klient_testowy_do_zadania_4()
    else:
        print("Niepoprawny wybór.")