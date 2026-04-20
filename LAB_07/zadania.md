<b><u>Uwaga</u></b> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

# Dane wspólne

```python
HOST = "interia.pl"          # albo 212.182.24.27
PORT = 110
USER = "twoj_login"
PASSWORD = "twoje_haslo"
```

---

1. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile wiadomości znajduje się w skrzynce.

```bash
telnet interia.pl 110
USER twoj_login
PASS twoje_haslo
STAT
QUIT
```

`STAT` zwraca coś w stylu:

```text
+OK 17 22084
```

---

2. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile bajtów (w sumie) zajmują wiadomości znajdujące się w skrzynce.

```bash
telnet interia.pl 110
USER twoj_login
PASS twoje_haslo
STAT
QUIT
```

W odpowiedzi:

```text
+OK 17 22084
```

druga liczba to **łączny rozmiar wiadomości w bajtach**, czyli tutaj **22084 bajty**.

---

3. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile bajtów zajmuje każda wiadomość (z osobna) znajdująca się w skrzynce.

```bash
telnet interia.pl 110
USER twoj_login
PASS twoje_haslo
LIST
QUIT
```

`LIST` zwróci listę w stylu:

```text
+OK scan listing follows
1 1319
2 1319
3 1319
...
.
```

Każda linia ma:

* numer wiadomości,
* rozmiar w bajtach.

---

4. Wykorzystując protokół telnet, oraz wybrany serwer POP3, wyświetl treść wiadomości o największym rozmiarze.

Sprawdzenie rozmiarów:

```bash
telnet interia.pl 110
USER twoj_login
PASS twoje_haslo
LIST
```

Wybór numeru największej wiadomości i pobranie jej:

```bash
RETR numer_wiadomosci
QUIT
```

Na przykład:

```bash
RETR 2
```

---

5. Wykorzystując protokół telnet, oraz wybrany serwer POP3, usuń wiadomość o najmniejszym rozmiarze.

```bash
telnet interia.pl 110
USER twoj_login
PASS twoje_haslo
LIST
```

Znalezienie najmniejszej wiadomości:

```bash
DELE numer_wiadomosci
QUIT
```

`Ważne`: w POP3 usunięcie wiadomości jest zatwierdzane dopiero po `QUIT`.

---

# Wspólna część do zadań 6–11

Zamiast powtarzać cały kod, użyj tego pomocniczego klienta POP3.

## Pomocniczy klient POP3

```python
import socket

HOST = "interia.pl"   # albo 212.182.24.27
PORT = 110
USER = "twoj_login"
PASSWORD = "twoje_haslo"

class POP3Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.file = self.sock.makefile("rb")
        print(self._readline())

    def _readline(self):
        line = self.file.readline()
        if not line:
            raise ConnectionError("Połączenie zostało zamknięte")
        return line.decode(errors="ignore").rstrip("\r\n")

    def command(self, cmd):
        self.sock.sendall((cmd + "\r\n").encode())
        return self._readline()

    def command_multi(self, cmd):
        first = self.command(cmd)
        lines = []

        if first.startswith("+OK"):
            while True:
                line = self._readline()
                if line == ".":
                    break
                if line.startswith(".."):
                    line = line[1:]
                lines.append(line)

        return first, lines

    def login(self, user, password):
        print(self.command(f"USER {user}"))
        print(self.command(f"PASS {password}"))

    def quit(self):
        print(self.command("QUIT"))
        self.file.close()
        self.sock.close()
```

---

6. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile wiadomości znajduje się w skrzynce.

```python
from pop3_client_base import POP3Client, HOST, PORT, USER, PASSWORD

client = POP3Client(HOST, PORT)
client.login(USER, PASSWORD)

response = client.command("STAT")
print(response)

parts = response.split()
print("Liczba wiadomości:", parts[1])

client.quit()
```

---

7. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile bajtów (w sumie) zajmują wiadomości znajdujące się w skrzynce.

```python
from pop3_client_base import POP3Client, HOST, PORT, USER, PASSWORD

client = POP3Client(HOST, PORT)
client.login(USER, PASSWORD)

response = client.command("STAT")
print(response)

parts = response.split()
print("Łączny rozmiar wiadomości w bajtach:", parts[2])

client.quit()
```

---

8. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile bajtów zajmuje każda wiadomość (z osobna) znajdująca się w skrzynce.

```python
from pop3_client_base import POP3Client, HOST, PORT, USER, PASSWORD

client = POP3Client(HOST, PORT)
client.login(USER, PASSWORD)

response, lines = client.command_multi("LIST")
print(response)

for line in lines:
    nr, size = line.split()
    print(f"Wiadomość {nr}: {size} bajtów")

client.quit()
```

---

9. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetl treść wiadomości o największym rozmiarze.

```python
from pop3_client_base import POP3Client, HOST, PORT, USER, PASSWORD

client = POP3Client(HOST, PORT)
client.login(USER, PASSWORD)

response, lines = client.command_multi("LIST")

wiadomosci = []
for line in lines:
    nr, size = line.split()
    wiadomosci.append((int(nr), int(size)))

numer_najwiekszej = max(wiadomosci, key=lambda x: x[1])[0]

print("Największa wiadomość ma numer:", numer_najwiekszej)

response, content = client.command_multi(f"RETR {numer_najwiekszej}")
print(response)
print("\n".join(content))

client.quit()
```

---

10. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli wszystkie wiadomości znajdujące się w skrzynce.

```python
from pop3_client_base import POP3Client, HOST, PORT, USER, PASSWORD

client = POP3Client(HOST, PORT)
client.login(USER, PASSWORD)

response, lines = client.command_multi("LIST")

numery = []
for line in lines:
    nr, _ = line.split()
    numery.append(int(nr))

for nr in numery:
    print(f"\n===== WIADOMOŚĆ {nr} =====")
    response, content = client.command_multi(f"RETR {nr}")
    print("\n".join(content))

client.quit()
```

---

11. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie pobierze z serwera wiadomość z załącznikiem (obrazkiem) i zapisze obrazek na dysk. Nazwa obrazka musi zgadzać się z nazwą załącznika podaną w mailu. Pamiętaj, że do przesyłania załączników binarnych w poczcie elektronicznej wykorzystywane jest kodowanie Base64.

```python
from pop3_client_base import POP3Client, HOST, PORT, USER, PASSWORD
from email import policy
from email.parser import BytesParser

client = POP3Client(HOST, PORT)
client.login(USER, PASSWORD)

response, lines = client.command_multi("LIST")

numery = []
for line in lines:
    nr, _ = line.split()
    numery.append(int(nr))

for nr in numery:
    response, content = client.command_multi(f"RETR {nr}")
    raw_message = ("\r\n".join(content) + "\r\n").encode()

    msg = BytesParser(policy=policy.default).parsebytes(raw_message)

    for part in msg.walk():
        filename = part.get_filename()
        content_type = part.get_content_type()

        if filename and content_type.startswith("image/"):
            data = part.get_payload(decode=True)
            with open(filename, "wb") as f:
                f.write(data)
            print("Zapisano załącznik:", filename)

client.quit()
```

---

12. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół POP3. Nie realizuj faktycznego pobierania e-maili, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient POP3 mógł pobrac wiadomosci. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.

Ten serwer:

* działa na `127.0.0.1`,
* obsługuje jednego klienta naraz,
* wspiera `USER`, `PASS`, `STAT`, `LIST`, `RETR`, `DELE`, `QUIT`,
* zwraca błąd dla nieznanej komendy,
* symuluje działanie POP3.

```python
import socket

HOST = "127.0.0.1"
PORT = 8110

POP3_USER = "student"
POP3_PASS = "haslo123"

MESSAGES = [
    "From: a@example.com\r\nTo: b@example.com\r\nSubject: Test 1\r\n\r\nTo jest pierwsza wiadomość.",
    "From: c@example.com\r\nTo: d@example.com\r\nSubject: Test 2\r\n\r\nTo jest druga wiadomość."
]


def send_line(conn, text):
    conn.sendall((text + "\r\n").encode())


def read_line(file):
    line = file.readline()
    if not line:
        return None
    return line.decode(errors="ignore").rstrip("\r\n")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Serwer POP3 działa na {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print("Połączono z:", addr)

    file = conn.makefile("rb")
    authorized = False
    user_ok = False
    to_delete = set()

    send_line(conn, "+OK POP3 server ready")

    while True:
        line = read_line(file)
        if line is None:
            break

        print("C:", line)

        parts = line.split(" ", 1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ""

        active_messages = [m for i, m in enumerate(MESSAGES) if i not in to_delete]

        if cmd == "USER":
            if arg == POP3_USER:
                user_ok = True
                send_line(conn, "+OK user accepted")
            else:
                send_line(conn, "-ERR invalid username")

        elif cmd == "PASS":
            if user_ok and arg == POP3_PASS:
                authorized = True
                send_line(conn, "+OK mailbox locked and ready")
            else:
                send_line(conn, "-ERR invalid password")

        elif not authorized:
            send_line(conn, "-ERR authorize first")

        elif cmd == "STAT":
            count = len(active_messages)
            size = sum(len(m.encode()) for m in active_messages)
            send_line(conn, f"+OK {count} {size}")

        elif cmd == "LIST":
            if arg:
                nr = int(arg)
                real_indexes = [i for i in range(len(MESSAGES)) if i not in to_delete]
                if 1 <= nr <= len(real_indexes):
                    idx = real_indexes[nr - 1]
                    size = len(MESSAGES[idx].encode())
                    send_line(conn, f"+OK {nr} {size}")
                else:
                    send_line(conn, "-ERR no such message")
            else:
                send_line(conn, f"+OK {len(active_messages)} messages")
                nr = 1
                for i, msg in enumerate(MESSAGES):
                    if i not in to_delete:
                        send_line(conn, f"{nr} {len(msg.encode())}")
                        nr += 1
                send_line(conn, ".")

        elif cmd == "RETR":
            nr = int(arg)
            real_indexes = [i for i in range(len(MESSAGES)) if i not in to_delete]
            if 1 <= nr <= len(real_indexes):
                idx = real_indexes[nr - 1]
                send_line(conn, f"+OK {len(MESSAGES[idx].encode())} octets")
                conn.sendall(MESSAGES[idx].encode() + b"\r\n.\r\n")
            else:
                send_line(conn, "-ERR no such message")

        elif cmd == "DELE":
            nr = int(arg)
            real_indexes = [i for i in range(len(MESSAGES)) if i not in to_delete]
            if 1 <= nr <= len(real_indexes):
                idx = real_indexes[nr - 1]
                to_delete.add(idx)
                send_line(conn, "+OK message deleted")
            else:
                send_line(conn, "-ERR no such message")

        elif cmd == "RSET":
            to_delete.clear()
            send_line(conn, "+OK reset")

        elif cmd == "QUIT":
            for idx in sorted(to_delete, reverse=True):
                del MESSAGES[idx]
            send_line(conn, "+OK bye")
            break

        else:
            send_line(conn, "-ERR command not supported")

    conn.close()
```

---

# Jak przetestować zadanie 12

W terminalu:

```bash
telnet 127.0.0.1 8110
```

Potem:

```text
USER student
PASS haslo123
STAT
LIST
RETR 1
DELE 1
QUIT
```