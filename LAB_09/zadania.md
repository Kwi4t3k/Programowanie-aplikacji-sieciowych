<b><u>Uwaga</u></b> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

# Dane wspólne

```python
HTTPBIN_HOST = "httpbin.org"
HTTPBIN_PORT = 80

TEST_HOST = "212.182.24.27"
TEST_PORT = 8080

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 8080
````

---

## 1. Pod adresem httpbin.org na porcie TCP o numerze 80 działa serwer obsługujący protokół HTTP w wersji 1.1. Pod odnośnikiem `/html` udostępnia prostą stronę HTML. Napisz program klienta, który połączy się z serwerem, a następnie pobierze treść strony i zapisze ją na dysku jako plik z rozszerzeniem `.html`. Spraw, aby serwer myślał, że żądanie przyszło od przeglądarki Safari 7.0.3. Jakich nagłówków HTTP należy użyć?

### Kod

```python
request = (
    "GET /html HTTP/1.1\r\n"
    "Host: httpbin.org\r\n"
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) "
    "AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0.3 Safari/537.71\r\n"
    "Connection: close\r\n"
    "\r\n"
)
```

### Użyte nagłówki

* `Host`
* `User-Agent`
* `Connection: close`

### Wynik

Program pobiera stronę HTML i zapisuje ją do pliku, np. `zad1_httpbin_html.html`.

---

## 2. Pod adresem httpbin.org na porcie TCP o numerze 80 działa serwer obsługujący protokół HTTP w wersji 1.1. Pod odnośnikiem `/image/png` udostępnia obrazek. Napisz program klienta, który połączy się z serwerem, a następnie pobierze obrazek i zapisze go na dysku. Jakich nagłówków HTTP należy użyć?

### Kod

```python
request = (
    "GET /image/png HTTP/1.1\r\n"
    "Host: httpbin.org\r\n"
    "Connection: close\r\n"
    "\r\n"
)
```

### Użyte nagłówki

* `Host`
* `Connection: close`

### Wynik

Program pobiera obrazek PNG i zapisuje go do pliku, np. `zad2_obrazek.png`.

---

## 3. Pod adresem 212.182.24.27 na porcie TCP o numerze 8080 działa serwer obsługujący protokół HTTP w wersji 1.1. Pod odnośnikiem `/image` udostępnia obrazek. Napisz program klienta, który połączy się z serwerem, a następnie pobierze z serwera obrazek w 3 częściach i po odebraniu wszystkich części złoży go w całość. Jakich nagłówków HTTP należy użyć?

### Kod

```python
request = (
    "GET /image HTTP/1.1\r\n"
    "Host: 212.182.24.27\r\n"
    "Connection: close\r\n"
    "\r\n"
)
```

### Użyte nagłówki

* `Host`
* `Connection: close`

### Wynik

Program odbiera odpowiedź w kilku fragmentach, łączy wszystkie odebrane części i zapisuje obrazek, np. jako `zad3_obrazek.jpg`.

---

## 4. Pod adresem httpbin.org na porcie TCP o numerze 80 działa serwer obsługujący protokół HTTP w wersji 1.1. Pod odnośnikiem `/post` udostępnia formularz z polami do wypełnienia. Napisz program klienta, który połączy się z serwerem, a następnie uzupełni formularz danymi pobranymi od użytkownika, a następnie prześle go do serwera i odbierze odpowiedź.

### Kod

```python
body = f"imie={imie}&nazwisko={nazwisko}&email={email}"

request = (
    "POST /post HTTP/1.1\r\n"
    "Host: httpbin.org\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    f"Content-Length: {len(body.encode())}\r\n"
    "Connection: close\r\n"
    "\r\n"
    f"{body}"
)
```

### Użyte nagłówki

* `Host`
* `Content-Type: application/x-www-form-urlencoded`
* `Content-Length`
* `Connection: close`

### Wynik

Program wysyła dane formularza metodą `POST`, a serwer odsyła odpowiedź zawierającą odebrane pola.

---

## 5. Slowloris

Atak Slowloris polega na:

* utworzeniu dużej liczby połączeń TCP,
* wysłaniu niepełnych nagłówków HTTP,
* bardzo powolnym dosyłaniu kolejnych linii nagłówków,
* utrzymywaniu połączeń otwartych jak najdłużej.

W efekcie serwer utrzymuje wiele częściowo zajętych połączeń i może przestać obsługiwać zwykłych klientów.

Slowloris nie wymaga dużej przepustowości sieciowej, lecz wykorzystuje ograniczoną liczbę połączeń po stronie serwera.

---

## 6. Zmodyfikuj program numer 3 z laboratorium numer 9 w taki sposób, aby program pobierał z serwera obrazek tylko wtedy, gdy zmienił się on od ostatniego pobrania. Jakich nagłówków HTTP należy użyć?

### Użyte nagłówki

* `If-Modified-Since`
* `If-None-Match`

### Kod – idea

```python
request = (
    "GET /image HTTP/1.1\r\n"
    "Host: 212.182.24.27\r\n"
    "If-None-Match: <etag_z_poprzedniej_odpowiedzi>\r\n"
    "If-Modified-Since: <last_modified_z_poprzedniej_odpowiedzi>\r\n"
    "Connection: close\r\n"
    "\r\n"
)
```

### Wynik

* jeśli obrazek się nie zmienił, serwer może zwrócić `304 Not Modified`,
* jeśli obrazek się zmienił, serwer zwróci `200 OK` i nową treść.

---

## 7. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, będzie serwerem HTTP. Obsłuży wybrane nagłówki i co najmniej jeden kod błędu (np. 404). Jako przykładowe pliki serwera (stronę główną i stronę błędu) możesz wykorzystać pliki `index.html`, `400.html`, `404.html`.

### Kod serwera

```python
import socket

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 8080

def recv_all(sock):
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def load_file_bytes(path):
    with open(path, "rb") as f:
        return f.read()

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCAL_HOST, LOCAL_PORT))
server.listen(1)

print(f"Serwer HTTP działa na {LOCAL_HOST}:{LOCAL_PORT}")

while True:
    conn, addr = server.accept()
    data = recv_all(conn)
    text = data.decode(errors="ignore")

    try:
        lines = text.split("\r\n")
        if not lines or len(lines[0].split()) != 3:
            body = load_file_bytes("400.html")
            response = build_response("HTTP/1.1 400 Bad Request", body, "text/html; charset=utf-8")
            conn.sendall(response)
            conn.close()
            continue

        method, path, version = lines[0].split()

        if method != "GET":
            body = load_file_bytes("400.html")
            response = build_response("HTTP/1.1 400 Bad Request", body, "text/html; charset=utf-8")
            conn.sendall(response)
            conn.close()
            continue

        if path == "/" or path == "/index.html":
            body = load_file_bytes("index.html")
            response = build_response("HTTP/1.1 200 OK", body, "text/html; charset=utf-8")
        else:
            body = load_file_bytes("404.html")
            response = build_response("HTTP/1.1 404 Not Found", body, "text/html; charset=utf-8")

        conn.sendall(response)
    except:
        try:
            body = load_file_bytes("400.html")
            response = build_response("HTTP/1.1 400 Bad Request", body, "text/html; charset=utf-8")
            conn.sendall(response)
        except:
            pass

    conn.close()
```

### Jak przetestować

```bash
telnet 127.0.0.1 8080
```

Przykładowe żądanie poprawne:

```text
GET /index.html HTTP/1.1
Host: 127.0.0.1
```

Przykładowe żądanie błędne:

```text
GET /brak.html HTTP/1.1
Host: 127.0.0.1
```

### Wynik przykładowy

* dla `/index.html` serwer zwraca `200 OK`,
* dla nieistniejącego pliku serwer zwraca `404 Not Found`,
* dla błędnego żądania serwer zwraca `400 Bad Request`.