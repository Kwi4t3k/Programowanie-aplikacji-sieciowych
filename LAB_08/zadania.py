import socket
import re

# DANE WSPÓLNE
HOST = "212.182.24.27"
PORT = 143
USER = "twoj_login"
PASSWORD = "twoje_haslo"

# POMOCNICZY KLIENT IMAP
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

# ZADANIE 2
def zadanie_2():
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

# ZADANIE 3
def zadanie_3():
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

# ZADANIE 4
def zadanie_4():
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

# ZADANIE 5
def zadanie_5():
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

# ZADANIE 6
def uruchom_serwer_imap():
    host = "127.0.0.1"
    port = 8143

    imap_user = "student"
    imap_pass = "haslo123"

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
    server.bind((host, port))
    server.listen(1)

    print(f"Serwer IMAP działa na {host}:{port}")

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
                if len(args) >= 2 and args[0] == imap_user and args[1] == imap_pass:
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

if __name__ == "__main__":
    print("Wybierz zadanie:")
    print("1 - instrukcja do zadania 1 (telnet)")
    print("2 - liczba wiadomości w Inbox")
    print("3 - liczba wiadomości we wszystkich skrzynkach")
    print("4 - nieprzeczytane wiadomości + oznacz jako przeczytane")
    print("5 - usuń wiadomość")
    print("6 - uruchom serwer IMAP")

    wybor = input("Twój wybór: ").strip()

    if wybor == "2":
        zadanie_2()
    elif wybor == "3":
        zadanie_3()
    elif wybor == "4":
        zadanie_4()
    elif wybor == "5":
        zadanie_5()
    elif wybor == "6":
        uruchom_serwer_imap()
    else:
        print("Niepoprawny wybór.")