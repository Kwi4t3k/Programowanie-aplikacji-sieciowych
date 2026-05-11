<b><u>Uwaga</u></b> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

# Dane wspólne

```python
WS_HOST = "localhost"
WS_PORT = 10000
WS_PATH = "/.ws"

LOCAL_WS_HOST = "127.0.0.1"
LOCAL_WS_PORT = 9001
````

## Przygotowanie lokalnego echo-servera

Uruchom echo-server lokalnie za pomocą Dockera:

```bash
docker run --detach -p 10000:8080 jmalloc/echo-server
```

Do testów przyjmujemy lokalny endpoint:

```text
ws://localhost:10000/.ws
```

---

## Wspólna część do zadań 1–3

### Pomocnicze funkcje WebSocket

```python
import socket
import base64
import hashlib
import os

WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

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
    frame.append(0x81)

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
```

---

## 1. Napisz program klienta, który nawiąże połączenie (handshake) z serwerem obsługującym protokół WebSocket, działającym pod adresem ws://echo.websocket.org na porcie 80.

W praktyce do testów użyto lokalnego echo-servera Docker pod adresem:

```text
ws://localhost:10000/.ws
```

### Kod

```python
sock = websocket_handshake("localhost", 10000, "/.ws")
print("Handshake zakończony poprawnie.")
close_ws(sock)
```

### Wynik przykładowy

```text
=== REQUEST ===
GET /.ws HTTP/1.1
Host: localhost:10000
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: ...
Sec-WebSocket-Version: 13
Origin: http://localhost:10000

=== RESPONSE ===
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: ...

Handshake zakończony poprawnie.
```

---

## 2. Napisz program klienta, który nawiąże połączenie (handshake) z serwerem obsługującym protokół WebSocket, działającym pod adresem ws://echo.websocket.org na porcie 80, a następnie, po nawiązaniu połączenia, wyśle do niego krótką (nie dłuższą niż 125 bajtów) wiadomość tekstową.

### Kod

```python
sock = websocket_handshake("localhost", 10000, "/.ws")

message = input("Podaj krótką wiadomość (<=125 bajtów): ")
frame = build_masked_text_frame(message)
sock.sendall(frame)

response = recv_ws_frame(sock)
print("Odpowiedź serwera:", response["payload"].decode(errors="ignore"))

close_ws(sock)
```

### Wynik przykładowy

```text
Podaj krótką wiadomość (<=125 bajtów): hello world
Odpowiedź serwera: hello world
```

---

## 3. Napisz program klienta, który nawiąże połączenie (handshake) z serwerem obsługującym protokół WebSocket, działającym pod adresem ws://echo.websocket.org na porcie 80, a następnie, po nawiązaniu połączenia, wyśle do niego wiadomość tekstową o dowolnej długości.

### Kod

```python
sock = websocket_handshake("localhost", 10000, "/.ws")

message = input("Podaj wiadomość dowolnej długości: ")
frame = build_masked_text_frame(message)
sock.sendall(frame)

response = recv_ws_frame(sock)
print("Odpowiedź serwera:", response["payload"].decode(errors="ignore"))

close_ws(sock)
```

### Wynik przykładowy

```text
Podaj wiadomość dowolnej długości: To jest dłuższa wiadomość testowa przesyłana przez WebSocket.
Odpowiedź serwera: To jest dłuższa wiadomość testowa przesyłana przez WebSocket.
```

---

## 4. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP będzie obsługiwał protokół WebSocket. Możesz ograniczyć się do wysyłania/odbierania danych w postaci tekstowej.

### Kod serwera

```python
import socket
import base64
import hashlib

LOCAL_WS_HOST = "127.0.0.1"
LOCAL_WS_PORT = 9001
WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

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

def compute_accept(key):
    raw = (key + WS_GUID).encode()
    sha1 = hashlib.sha1(raw).digest()
    return base64.b64encode(sha1).decode()

def build_unmasked_text_frame(text):
    payload = text.encode("utf-8")
    frame = bytearray()
    frame.append(0x81)

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

    return opcode, payload

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCAL_WS_HOST, LOCAL_WS_PORT))
server.listen(1)

print(f"Serwer WebSocket działa na {LOCAL_WS_HOST}:{LOCAL_WS_PORT}")

while True:
    conn, addr = server.accept()
    print("Połączono z:", addr)

    try:
        request = recv_until(conn, b"\r\n\r\n").decode(errors="ignore")

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

        while True:
            opcode, payload = recv_ws_frame(conn)

            if opcode == 0x8:
                break

            if opcode == 0x1:
                text = payload.decode(errors="ignore")
                print("Odebrano:", text)
                conn.sendall(build_unmasked_text_frame(text))

    except Exception as e:
        print("Błąd:", e)

    conn.close()
```

### Klient testowy do zadania 4

```python
sock = websocket_handshake("127.0.0.1", 9001, "/")

message = input("Podaj wiadomość do lokalnego serwera: ")
frame = build_masked_text_frame(message)
sock.sendall(frame)

response = recv_ws_frame(sock)
print("Odpowiedź serwera:", response["payload"].decode(errors="ignore"))

close_ws(sock)
```

### Wynik przykładowy

```text
Podaj wiadomość do lokalnego serwera: test lokalny
Odpowiedź serwera: test lokalny
```