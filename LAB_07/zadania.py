# zad 6

# from pomocniczy_klient import POP3Client, HOST, PORT, USER, PASSWORD

# client = POP3Client(HOST, PORT)
# client.login(USER, PASSWORD)

# response = client.command("STAT")
# print(response)

# parts = response.split()
# print("Liczba wiadomości:", parts[1])

# client.quit()

# zad 7

# from pomocniczy_klient import POP3Client, HOST, PORT, USER, PASSWORD

# client = POP3Client(HOST, PORT)
# client.login(USER, PASSWORD)

# response = client.command("STAT")
# print(response)

# parts = response.split()
# print("Łączny rozmiar wiadomości w bajtach:", parts[2])

# client.quit()

# zad 8

# from pomocniczy_klient import POP3Client, HOST, PORT, USER, PASSWORD

# client = POP3Client(HOST, PORT)
# client.login(USER, PASSWORD)

# response, lines = client.command_multi("LIST")
# print(response)

# for line in lines:
#     nr, size = line.split()
#     print(f"Wiadomość {nr}: {size} bajtów")

# client.quit()

# zad 9

# from pomocniczy_klient import POP3Client, HOST, PORT, USER, PASSWORD

# client = POP3Client(HOST, PORT)
# client.login(USER, PASSWORD)

# response, lines = client.command_multi("LIST")

# wiadomosci = []
# for line in lines:
#     nr, size = line.split()
#     wiadomosci.append((int(nr), int(size)))

# numer_najwiekszej = max(wiadomosci, key=lambda x: x[1])[0]

# print("Największa wiadomość ma numer:", numer_najwiekszej)

# response, content = client.command_multi(f"RETR {numer_najwiekszej}")
# print(response)
# print("\n".join(content))

# client.quit()

# zad 10

# from pomocniczy_klient import POP3Client, HOST, PORT, USER, PASSWORD

# client = POP3Client(HOST, PORT)
# client.login(USER, PASSWORD)

# response, lines = client.command_multi("LIST")

# numery = []
# for line in lines:
#     nr, _ = line.split()
#     numery.append(int(nr))

# for nr in numery:
#     print(f"\n===== WIADOMOŚĆ {nr} =====")
#     response, content = client.command_multi(f"RETR {nr}")
#     print("\n".join(content))

# client.quit()

# zad 11

# from pomocniczy_klient import POP3Client, HOST, PORT, USER, PASSWORD
# from email import policy
# from email.parser import BytesParser

# client = POP3Client(HOST, PORT)
# client.login(USER, PASSWORD)

# response, lines = client.command_multi("LIST")

# numery = []
# for line in lines:
#     nr, _ = line.split()
#     numery.append(int(nr))

# for nr in numery:
#     response, content = client.command_multi(f"RETR {nr}")
#     raw_message = ("\r\n".join(content) + "\r\n").encode()

#     msg = BytesParser(policy=policy.default).parsebytes(raw_message)

#     for part in msg.walk():
#         filename = part.get_filename()
#         content_type = part.get_content_type()

#         if filename and content_type.startswith("image/"):
#             data = part.get_payload(decode=True)
#             with open(filename, "wb") as f:
#                 f.write(data)
#             print("Zapisano załącznik:", filename)

# client.quit()

# zad 12

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