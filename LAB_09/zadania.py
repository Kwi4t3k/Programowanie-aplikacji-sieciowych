import socket
import os

# DANE WSPÓLNE
HTTPBIN_HOST = "httpbin.org"
HTTPBIN_PORT = 80

TEST_HOST = "212.182.24.27"
TEST_PORT = 8080

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 8080

CACHE_FILE = "image_cache_headers.txt"


# POMOCNICZE FUNKCJE HTTP
def recv_all(sock):
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def send_http_request(host, port, request_text):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(request_text.encode())
    response = recv_all(sock)
    sock.close()
    return response


def split_http_response(response_bytes):
    if b"\r\n\r\n" in response_bytes:
        header_bytes, body = response_bytes.split(b"\r\n\r\n", 1)
    else:
        header_bytes = response_bytes
        body = b""

    header_text = header_bytes.decode(errors="ignore")
    lines = header_text.split("\r\n")
    status_line = lines[0] if lines else ""
    headers = {}

    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

    return status_line, headers, body


def save_binary(filename, data):
    with open(filename, "wb") as f:
        f.write(data)


def save_text(filename, data):
    with open(filename, "w", encoding="utf-8", errors="ignore") as f:
        f.write(data.decode(errors="ignore"))


def print_response_summary(response_bytes):
    status_line, headers, body = split_http_response(response_bytes)
    print("STATUS:", status_line)
    print("HEADERS:")
    for k, v in headers.items():
        print(f"{k}: {v}")
    print("BODY LENGTH:", len(body))

# ZADANIE 1
def zadanie_1():
    request = (
        "GET /html HTTP/1.1\r\n"
        f"Host: {HTTPBIN_HOST}\r\n"
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) "
        "AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0.3 Safari/537.71\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    response = send_http_request(HTTPBIN_HOST, HTTPBIN_PORT, request)
    status_line, headers, body = split_http_response(response)

    print(status_line)
    save_text("zad1_httpbin_html.html", body)
    print("Zapisano plik: zad1_httpbin_html.html")

# ZADANIE 2
def zadanie_2():
    request = (
        "GET /image/png HTTP/1.1\r\n"
        f"Host: {HTTPBIN_HOST}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    response = send_http_request(HTTPBIN_HOST, HTTPBIN_PORT, request)
    status_line, headers, body = split_http_response(response)

    print(status_line)
    save_binary("zad2_obrazek.png", body)
    print("Zapisano plik: zad2_obrazek.png")

# ZADANIE 3
def zadanie_3():
    request = (
        "GET /image HTTP/1.1\r\n"
        f"Host: {TEST_HOST}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    response = send_http_request(TEST_HOST, TEST_PORT, request)
    status_line, headers, body = split_http_response(response)

    print(status_line)
    save_binary("zad3_obrazek.jpg", body)
    print("Zapisano plik: zad3_obrazek.jpg")

# ZADANIE 4
def zadanie_4():
    imie = input("Podaj imię: ").strip()
    nazwisko = input("Podaj nazwisko: ").strip()
    email = input("Podaj email: ").strip()

    body = f"imie={imie}&nazwisko={nazwisko}&email={email}"
    body_bytes = body.encode()

    request = (
        "POST /post HTTP/1.1\r\n"
        f"Host: {HTTPBIN_HOST}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )

    response = send_http_request(HTTPBIN_HOST, HTTPBIN_PORT, request)
    status_line, headers, response_body = split_http_response(response)

    print(status_line)
    print(response_body.decode(errors="ignore"))

# ZADANIE 6
def read_cache_headers():
    headers = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    k, v = line.strip().split(":", 1)
                    headers[k] = v
    return headers


def save_cache_headers(headers):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        if "ETag" in headers:
            f.write(f"ETag:{headers['ETag']}\n")
        if "Last-Modified" in headers:
            f.write(f"Last-Modified:{headers['Last-Modified']}\n")


def zadanie_6():
    cached = read_cache_headers()

    request = (
        "GET /image HTTP/1.1\r\n"
        f"Host: {TEST_HOST}\r\n"
    )

    if "ETag" in cached:
        request += f"If-None-Match: {cached['ETag']}\r\n"
    if "Last-Modified" in cached:
        request += f"If-Modified-Since: {cached['Last-Modified']}\r\n"

    request += "Connection: close\r\n\r\n"

    response = send_http_request(TEST_HOST, TEST_PORT, request)
    status_line, headers, body = split_http_response(response)

    print(status_line)

    if "304" in status_line:
        print("Obrazek nie zmienił się od ostatniego pobrania.")
    elif "200" in status_line:
        save_binary("zad6_obrazek.jpg", body)
        save_cache_headers(headers)
        print("Pobrano nową wersję obrazka i zapisano jako zad6_obrazek.jpg")
    else:
        print("Serwer zwrócił inną odpowiedź:", status_line)

# ZADANIE 7
def guess_content_type(path):
    lower = path.lower()
    if lower.endswith(".html"):
        return "text/html; charset=utf-8"
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return "image/jpeg"
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".gif"):
        return "image/gif"
    return "application/octet-stream"


def build_response(status_line, body, content_type):
    headers = [
        status_line,
        "Server: PAS/2017 HTTP Server",
        f"Content-Length: {len(body)}",
        f"Content-Type: {content_type}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode() + body


def load_file_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def zadanie_7_serwer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCAL_HOST, LOCAL_PORT))
    server.listen(1)

    print(f"Serwer HTTP działa na {LOCAL_HOST}:{LOCAL_PORT}")

    while True:
        conn, addr = server.accept()
        print("Połączono z:", addr)

        data = recv_all(conn)
        text = data.decode(errors="ignore")
        print("ODEBRANO ŻĄDANIE:")
        print(text)

        try:
            lines = text.split("\r\n")
            if not lines or len(lines[0].split()) != 3:
                body = load_file_bytes("400.html")
                response = build_response(
                    "HTTP/1.1 400 Bad Request",
                    body,
                    "text/html; charset=utf-8"
                )
                conn.sendall(response)
                conn.close()
                continue

            method, path, version = lines[0].split()

            if method != "GET":
                body = load_file_bytes("400.html")
                response = build_response(
                    "HTTP/1.1 400 Bad Request",
                    body,
                    "text/html; charset=utf-8"
                )
                conn.sendall(response)
                conn.close()
                continue

            if path == "/" or path == "/index.html":
                body = load_file_bytes("index.html")
                response = build_response(
                    "HTTP/1.1 200 OK",
                    body,
                    "text/html; charset=utf-8"
                )
            else:
                body = load_file_bytes("404.html")
                response = build_response(
                    "HTTP/1.1 404 Not Found",
                    body,
                    "text/html; charset=utf-8"
                )

            conn.sendall(response)

        except Exception as e:
            print("Błąd:", e)
            try:
                body = load_file_bytes("400.html")
                response = build_response(
                    "HTTP/1.1 400 Bad Request",
                    body,
                    "text/html; charset=utf-8"
                )
                conn.sendall(response)
            except:
                pass

        conn.close()

if __name__ == "__main__":
    print("Wybierz zadanie:")
    print("1 - pobierz /html z httpbin.org i zapisz jako HTML")
    print("2 - pobierz /image/png z httpbin.org")
    print("3 - pobierz obrazek z 212.182.24.27:8080/image")
    print("4 - wyślij formularz POST do httpbin.org/post")
    print("6 - warunkowe pobieranie obrazka (If-Modified-Since / If-None-Match)")
    print("7 - uruchom lokalny serwer HTTP")

    wybor = input("Twój wybór: ").strip()

    if wybor == "1":
        zadanie_1()
    elif wybor == "2":
        zadanie_2()
    elif wybor == "3":
        zadanie_3()
    elif wybor == "4":
        zadanie_4()
    elif wybor == "6":
        zadanie_6()
    elif wybor == "7":
        zadanie_7_serwer()
    else:
        print("Niepoprawny wybór.")