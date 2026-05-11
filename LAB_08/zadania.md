<b><u>Uwaga</u></b> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

# Dane wspólne

```python
HOST = "212.182.24.27"
PORT = 143
USER = "twoj_login"
PASSWORD = "twoje_haslo"
````

---

## 1. Wykorzystując protokół telnet, oraz serwer IMAP, zaloguj się do skrzynki i sprawdź, ile wiadomości znajduje się w poszczególnych skrzynkach. Pobierz pierwszą dostępną wiadomość, i oznacz ją jako przeczytaną. Wykorzystaj komendę protokołu IMAP - STORE.

### Polecenia

```bash
telnet 212.182.24.27 143
A1 LOGIN twoj_login twoje_haslo
A2 LIST "" "*"
A3 SELECT INBOX
A4 SEARCH ALL
A5 FETCH 1 BODY[]
A6 STORE 1 +FLAGS \Seen
A7 LOGOUT
```

### Opis

* `LOGIN` – logowanie do serwera
* `LIST "" "*"` – wyświetlenie wszystkich skrzynek
* `SELECT INBOX` – wybór skrzynki Inbox
* `SEARCH ALL` – pobranie identyfikatorów wiadomości
* `FETCH 1 BODY[]` – pobranie pierwszej wiadomości
* `STORE 1 +FLAGS \Seen` – oznaczenie wiadomości jako przeczytanej
* `LOGOUT` – wylogowanie z serwera

### Wynik przykładowy

```text
* OK CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE AUTH=PLAIN AUTH=LOGIN
A1 OK Capability completed, logged in
* LIST (\HasNoChildren) "/" "INBOX"
A2 OK LIST completed
* 2 EXISTS
* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
A3 OK [READ-WRITE] Select completed
* SEARCH 1 2
A4 OK SEARCH completed
* 1 FETCH (BODY[] {36}
Test 1 Test 1 Test 1 Test 1
)
A5 OK FETCH completed
* 1 FETCH (FLAGS (\Seen))
A6 OK STORE completed
* BYE Logging out
A7 OK LOGOUT completed
```

---

## Wspólna część do zadań 2–5

### Pomocniczy klient IMAP

```python
import socket

HOST = "212.182.24.27"
PORT = 143
USER = "twoj_login"
PASSWORD = "twoje_haslo"


class IMAPClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.file = self.sock.makefile("rb")
        self.tag_counter = 1
        print(self._readline())

    def _readline(self):
        line = self.file.readline()
        if not line:
            raise ConnectionError("Połączenie zostało zamknięte")
        return line.decode(errors="ignore").rstrip("\r\n")

    def _next_tag(self):
        tag = f"A{self.tag_counter}"
        self.tag_counter += 1
        return tag

    def command(self, cmd):
        tag = self._next_tag()
        full_cmd = f"{tag} {cmd}\r\n"
        self.sock.sendall(full_cmd.encode())

        lines = []
        while True:
            line = self._readline()
            lines.append(line)
            if line.startswith(tag + " "):
                break

        return tag, lines

    def login(self, user, password):
        _, lines = self.command(f"LOGIN {user} {password}")
        for line in lines:
            print(line)

    def logout(self):
        _, lines = self.command("LOGOUT")
        for line in lines:
            print(line)
        self.file.close()
        self.sock.close()
```

---

## 2. Napisz program klienta, który połączy się z serwerem IMAP, a następnie wyświetli informację o tym, ile wiadomości znajduje się w skrzynce Inbox.

### Kod

```python
from imap_client_base import IMAPClient, HOST, PORT, USER, PASSWORD
import re

client = IMAPClient(HOST, PORT)
client.login(USER, PASSWORD)

tag, lines = client.command("STATUS INBOX (MESSAGES)")
for line in lines:
    print(line)

for line in lines:
    if line.startswith("* STATUS"):
        match = re.search(r"MESSAGES (\d+)", line)
        if match:
            print("Liczba wiadomości w Inbox:", match.group(1))

client.logout()
```

### Wynik przykładowy

```text
* STATUS Inbox (MESSAGES 2)
A2 OK STATUS completed
Liczba wiadomości w Inbox: 2
```

---

## 3. Napisz program klienta, który połączy się z serwerem IMAP, a następnie wyświetli informację o tym, ile wiadomości znajduje się we wszystkich skrzynkach łącznie.

### Kod

```python
from imap_client_base import IMAPClient, HOST, PORT, USER, PASSWORD
import re

client = IMAPClient(HOST, PORT)
client.login(USER, PASSWORD)

tag, lines = client.command('LIST "" "*"')

mailboxes = []
for line in lines:
    print(line)
    if line.startswith("* LIST"):
        parts = line.split(' "/" ')
        if len(parts) == 2:
            mailbox = parts[1].strip('"')
            mailboxes.append(mailbox)

suma = 0

for mailbox in mailboxes:
    tag, status_lines = client.command(f"STATUS {mailbox} (MESSAGES)")
    for line in status_lines:
        print(line)
        if line.startswith("* STATUS"):
            match = re.search(r"MESSAGES (\d+)", line)
            if match:
                suma += int(match.group(1))

print("Łączna liczba wiadomości we wszystkich skrzynkach:", suma)

client.logout()
```

### Wynik

Wynik zależy od zawartości skrzynki użytkownika.

---

## 4. Napisz program klienta, który połączy się z serwerem IMAP, a następnie sprawdzi, czy w skrzynce są nieprzeczytane wiadomości. Jeśli tak, wyświetli treść wszystkich nieprzeczytanych wiadomości oraz oznaczy je jako przeczytane (komenda STORE i flagi - FLAGS).

### Kod

```python
from imap_client_base import IMAPClient, HOST, PORT, USER, PASSWORD

client = IMAPClient(HOST, PORT)
client.login(USER, PASSWORD)

tag, lines = client.command("SELECT INBOX")
for line in lines:
    print(line)

tag, lines = client.command("SEARCH UNSEEN")
for line in lines:
    print(line)

numery = []
for line in lines:
    if line.startswith("* SEARCH"):
        parts = line.split()
        numery = parts[2:]

if not numery:
    print("Brak nieprzeczytanych wiadomości.")
else:
    print("Nieprzeczytane wiadomości:", ", ".join(numery))

    for nr in numery:
        print(f"\n===== WIADOMOŚĆ {nr} =====")
        tag, fetch_lines = client.command(f"FETCH {nr} BODY[TEXT]")
        for line in fetch_lines:
            print(line)

        tag, store_lines = client.command(f"STORE {nr} +FLAGS \\Seen")
        for line in store_lines:
            print(line)

client.logout()
```

### Wynik przykładowy

```text
* SEARCH 1 3
A3 OK SEARCH completed
Nieprzeczytane wiadomości: 1, 3

===== WIADOMOŚĆ 1 =====
* 1 FETCH (BODY[TEXT] {27}
Treść pierwszej wiadomości
)
A4 OK FETCH completed
* 1 FETCH (FLAGS (\Seen))
A5 OK STORE completed
```

---

## 5. Napisz program klienta, który połączy się z serwerem IMAP, a następnie fizycznie usunie wybraną wiadomość.

### Kod

```python
from imap_client_base import IMAPClient, HOST, PORT, USER, PASSWORD

client = IMAPClient(HOST, PORT)
client.login(USER, PASSWORD)

tag, lines = client.command("SELECT INBOX")
for line in lines:
    print(line)

numer = input("Podaj numer wiadomości do usunięcia: ").strip()

tag, lines = client.command(f"STORE {numer} +FLAGS \\Deleted")
for line in lines:
    print(line)

tag, lines = client.command("EXPUNGE")
for line in lines:
    print(line)

client.logout()
```

### Wynik przykładowy

```text
* 2 FETCH (FLAGS (\Deleted))
A4 OK STORE completed
* 2 EXPUNGE
A5 OK EXPUNGE completed
```

---

## 6. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół IMAP. Nie realizuj faktycznego pobierania e-maili, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient IMAP mógł pobrac wiadomości. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.

### Kod serwera

```python
import socket

HOST = "127.0.0.1"
PORT = 8143

IMAP_USER = "student"
IMAP_PASS = "haslo123"

mailboxes = {
    "INBOX": [
        {"body": "To jest pierwsza wiadomość.", "flags": set()},
        {"body": "To jest druga wiadomość.", "flags": {"\\Seen"}},
        {"body": "To jest trzecia wiadomość.", "flags": set()},
    ],
    "Archive": [
        {"body": "Archiwalna wiadomość.", "flags": {"\\Seen"}}
    ]
}


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

print(f"Serwer IMAP działa na {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print("Połączono z:", addr)

    file = conn.makefile("rb")
    authorized = False
    selected_mailbox = None

    send_line(conn, "* OK IMAP4rev1 Service Ready")

    while True:
        line = read_line(file)
        if line is None:
            break

        print("C:", line)

        parts = line.split()
        if len(parts) < 2:
            send_line(conn, "* BAD invalid command")
            continue

        tag = parts[0]
        cmd = parts[1].upper()
        args = parts[2:]

        if cmd == "LOGIN":
            if len(args) >= 2 and args[0] == IMAP_USER and args[1] == IMAP_PASS:
                authorized = True
                send_line(conn, f"{tag} OK LOGIN completed")
            else:
                send_line(conn, f"{tag} NO LOGIN failed")

        elif not authorized:
            send_line(conn, f"{tag} NO authenticate first")

        elif cmd == "LIST":
            for mailbox in mailboxes.keys():
                send_line(conn, f'* LIST () "/" "{mailbox}"')
            send_line(conn, f"{tag} OK LIST completed")

        elif cmd == "SELECT":
            if not args:
                send_line(conn, f"{tag} BAD missing mailbox")
            else:
                mailbox = args[0].strip('"')
                if mailbox in mailboxes:
                    selected_mailbox = mailbox
                    messages = mailboxes[mailbox]
                    send_line(conn, f"* {len(messages)} EXISTS")
                    send_line(conn, "* FLAGS (\\Seen \\Deleted)")
                    send_line(conn, f"{tag} OK [READ-WRITE] SELECT completed")
                else:
                    send_line(conn, f"{tag} NO no such mailbox")

        elif cmd == "STATUS":
            if len(args) >= 2:
                mailbox = args[0].strip('"')
                if mailbox in mailboxes:
                    count = len(mailboxes[mailbox])
                    send_line(conn, f'* STATUS {mailbox} (MESSAGES {count})')
                    send_line(conn, f"{tag} OK STATUS completed")
                else:
                    send_line(conn, f"{tag} NO no such mailbox")
            else:
                send_line(conn, f"{tag} BAD invalid STATUS")

        elif cmd == "SEARCH":
            if selected_mailbox is None:
                send_line(conn, f"{tag} NO select mailbox first")
            else:
                msgs = mailboxes[selected_mailbox]

                if args and args[0].upper() == "ALL":
                    ids = [str(i + 1) for i in range(len(msgs))]
                elif args and args[0].upper() == "UNSEEN":
                    ids = [str(i + 1) for i, msg in enumerate(msgs) if "\\Seen" not in msg["flags"]]
                else:
                    ids = []

                send_line(conn, "* SEARCH " + " ".join(ids))
                send_line(conn, f"{tag} OK SEARCH completed")

        elif cmd == "FETCH":
            if selected_mailbox is None:
                send_line(conn, f"{tag} NO select mailbox first")
            elif len(args) < 2:
                send_line(conn, f"{tag} BAD invalid FETCH")
            else:
                nr = int(args[0])
                what = " ".join(args[1:])
                msgs = mailboxes[selected_mailbox]

                if 1 <= nr <= len(msgs):
                    msg = msgs[nr - 1]
                    body = msg["body"]

                    if "BODY[TEXT]" in what or "BODY[]" in what:
                        send_line(conn, f'* {nr} FETCH (BODY[TEXT] {{{len(body)}}}')
                        send_line(conn, body)
                        send_line(conn, ")")
                        send_line(conn, f"{tag} OK FETCH completed")
                    elif "FLAGS" in what:
                        flags = " ".join(msg["flags"])
                        send_line(conn, f'* {nr} FETCH (FLAGS ({flags}))')
                        send_line(conn, f"{tag} OK FETCH completed")
                    else:
                        send_line(conn, f"{tag} BAD unsupported FETCH")
                else:
                    send_line(conn, f"{tag} NO no such message")

        elif cmd == "STORE":
            if selected_mailbox is None:
                send_line(conn, f"{tag} NO select mailbox first")
            elif len(args) < 3:
                send_line(conn, f"{tag} BAD invalid STORE")
            else:
                nr = int(args[0])
                op = args[1]
                flag = args[2]
                msgs = mailboxes[selected_mailbox]

                if 1 <= nr <= len(msgs):
                    if op == "+FLAGS":
                        msgs[nr - 1]["flags"].add(flag)
                    elif op == "-FLAGS" and flag in msgs[nr - 1]["flags"]:
                        msgs[nr - 1]["flags"].remove(flag)

                    flags = " ".join(msgs[nr - 1]["flags"])
                    send_line(conn, f'* {nr} FETCH (FLAGS ({flags}))')
                    send_line(conn, f"{tag} OK STORE completed")
                else:
                    send_line(conn, f"{tag} NO no such message")

        elif cmd == "EXPUNGE":
            if selected_mailbox is None:
                send_line(conn, f"{tag} NO select mailbox first")
            else:
                msgs = mailboxes[selected_mailbox]
                new_msgs = []
                nr = 1
                for msg in msgs:
                    if "\\Deleted" in msg["flags"]:
                        send_line(conn, f"* {nr} EXPUNGE")
                    else:
                        new_msgs.append(msg)
                        nr += 1
                mailboxes[selected_mailbox] = new_msgs
                send_line(conn, f"{tag} OK EXPUNGE completed")

        elif cmd == "LOGOUT":
            send_line(conn, "* BYE Logging out")
            send_line(conn, f"{tag} OK LOGOUT completed")
            break

        else:
            send_line(conn, f"{tag} BAD command not supported")

    conn.close()
```

### Jak przetestować

```bash
telnet 127.0.0.1 8143
```

Następnie:

```text
A1 LOGIN student haslo123
A2 LIST "" "*"
A3 STATUS INBOX (MESSAGES)
A4 SELECT INBOX
A5 SEARCH ALL
A6 FETCH 1 BODY[TEXT]
A7 STORE 1 +FLAGS \Seen
A8 STORE 1 +FLAGS \Deleted
A9 EXPUNGE
A10 LOGOUT
```

### Wynik przykładowy

```text
* OK IMAP4rev1 Service Ready
A1 OK LOGIN completed
* LIST () "/" "INBOX"
* LIST () "/" "Archive"
A2 OK LIST completed
* STATUS INBOX (MESSAGES 3)
A3 OK STATUS completed
* 3 EXISTS
* FLAGS (\Seen \Deleted)
A4 OK [READ-WRITE] SELECT completed
* SEARCH 1 2 3
A5 OK SEARCH completed
* 1 FETCH (BODY[TEXT] {27}
To jest pierwsza wiadomość.
)
A6 OK FETCH completed
* 1 FETCH (FLAGS (\Seen))
A7 OK STORE completed
* 1 FETCH (FLAGS (\Deleted \Seen))
A8 OK STORE completed
* 1 EXPUNGE
A9 OK EXPUNGE completed
* BYE Logging out
A10 OK LOGOUT completed
```

```