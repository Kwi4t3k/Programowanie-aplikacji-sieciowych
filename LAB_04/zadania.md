> Uwaga! W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

---

1. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, dla podłączającego się klienta, będzie odsyłał mu aktualny czas oraz datę. Prawidłowa komunikacja powinna odbywać się w nastepujacy sposób:
- Serwer odbiera od klienta wiadomość (dowolną)
- Serwer odsyła klientowi aktualną datę i czas

```python
import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serwer.bind((HOST, PORT))
serwer.listen(1)

print("Uruchomiono serwer...")

while True:
    klient, adres = serwer.accept()
    print("Połączono z:", adres)

    dane = klient.recv(1024)

    if dane:
        teraz = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        klient.send(teraz.encode())

    klient.close()
```

---

2. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, dla podłączającego się klienta, będzie odsyłał mu przesłaną wiadomość (tzw. serwer echa). Prawidłowa komunikacja
powinna odbywać się w nastepujacy sposób:
- Serwer odbiera dane od klienta
- Serwer odsyła klientowi odebrane od niego dane

```python
import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serwer.bind((HOST, PORT))
serwer.listen(1)

print("Uruchomiono serwer...")

while True:
    klient, adres = serwer.accept()
    print("Połączono z:", adres)

    dane = klient.recv(1024)

    if(dane):
        klient.send(dane)

    klient.close()
```

---

3. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, będzie odsyłał mu przesłaną wiadomość (tzw. serwer echa). Prawidłowa komunikacja powinna odbywać się w nastepujacy sposób:
- Serwer odbiera dane od klienta
- Serwer odsyła klientowi odebrane od niego dane

```python
import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer...")

while True:
    dane, adres = serwer.recvfrom(1024)
    print("Odebrano wiadomość od:", adres)

    if dane:
        serwer.sendto(dane, adres)
```

---

4. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, będzie odbierał liczbę, operator i liczbę, a następnie odsyłał użytkownikowi wynik działania, przez niego przesłanego.

```python
import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer...")

while True:
    dane, adres = serwer.recvfrom(1024)
    wiadomosc = dane.decode().strip()
    print("Odebrano wiadomość od:", adres)
    czesci = wiadomosc.split()

    if len(czesci) != 3:
        wynik = "Użyj liczba -> operator -> liczba"
    else:
        liczba1, operator, liczba2 = czesci

        try:
            liczba1 = float(liczba1)
            liczba2 = float(liczba2)

            if operator == "+":
                wynik = str(liczba1 + liczba2)
            elif operator == "-":
                wynik = str(liczba1 + liczba2)
            elif operator == "*":
                wynik = str(liczba1 * liczba2)
            elif operator == "/":
                if liczba2 == 0:
                    wynik = "Nie można dzielić przez zero"
                else:
                    wynik = str(liczba1 / liczba2)
            else:
                wynik = "Nieznany operator"
        except ValueError:
            wynik = "Błędne dane"

    serwer.sendto(wynik.encode(), adres)
```

---

5. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego adres IP, i odeśle odpowiadającą mu nazwę hostname.

```python
import socket

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer...")

while True:
    dane, adres = serwer.recvfrom(1024)
    ip = dane.decode().strip()

    print("Odebrano od", adres, "IP:", ip)

    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        hostname = "Nie znaleziono hostname"

    serwer.sendto(hostname.encode(), adres)
```

---

6. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego nazwę hostname, i odeśle odpowiadający mu adres IP.

```python
import socket

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer...")

while True:
    dane, adres = serwer.recvfrom(1024)
    hostname = dane.decode().strip()

    print("Odebrano od", adres, "hostname:", hostname)

    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip = "Nie znaleziono IP"

    serwer.sendto(ip.encode(), adres)
```

---

7. Zmodyfikuj program nr 2 z laboratorium nr 3 w ten sposób, aby serwer wysyłał i odbierał wiadomość o maksymalnej długości 20 znaków.

```python
import socket, select
from time import gmtime, strftime

HOST = '127.0.0.1'
PORT = 2900

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)

print("[%s] TCP ECHO Server is waiting for incoming connections on port %s ... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), PORT))

while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:

        if sock == server_socket:

            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)

            print("[%s] Client %s connected ... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))

        else:
            try:
                data = sock.recv(4096)
                if data:
                    message = data.decode()

                    if len(message) > 20:
                        message = message[:20]

                    sock.send(message.encode())

                    print("[%s] Sending back to client %s data: ['%s']... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address, message))
                else:
                    print("[%s] Client (%s) is offline" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))
                    sock.close()
                    connected_clients_sockets.remove(sock)
                    continue

            except:
                print("[%s] Client (%s) is offline" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))
                sock.close()
                connected_clients_sockets.remove(sock)
                continue

server_socket.close()
```

---

8. Zmodyfikuj program nr 7 z laboratorium nr 3 w ten sposób, aby mieć pewność, że serwer w rzeczywistości odebrał / wysłał wiadomość o wymaganej długości.

```python
import socket

HOST = "127.0.0.1"
PORT = 2900

def recvall(sock, msgLen):
    msg = b""
    bytesRcvd = 0

    while bytesRcvd < msgLen:
        chunk = sock.recv(msgLen - bytesRcvd)

        if chunk == b"":
            break

        bytesRcvd += len(chunk)
        msg += chunk

    return msg

serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serwer.bind((HOST, PORT))
serwer.listen(1)

print("Uruchomiono serwer...")

while True:
    klient, adres = serwer.accept()
    print("Połączono z:", adres)

    dane = recvall(klient, 20)

    if dane:
        print("Odebrano:", dane.decode(errors="ignore"))
        klient.sendall(dane)

    klient.close()
```

---

9. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego wiadomość o treści podanej w zadaniu nr 13 z laboratorium nr 3, a następnie odeśle klientowi odpowiedź TAK lub NIE. W przypadku błędnego sformatowania wiadomości, serwer odeśle klientowi odpowiedź BAD SYNTAX.

```python
import socket

HOST = "127.0.0.1"
PORT = 2910

def check_msg_syntax(txt):
    parts = txt.split(";")

    if len(parts) != 7:
        return "BAD_SYNTAX"

    if parts[0] != "zad13odp" or parts[1] != "src" or parts[3] != "dst" or parts[5] != "data":
        return "BAD_SYNTAX"

    try:
        src_port = int(parts[2])
        dst_port = int(parts[4])
        data_len = int(parts[6])
    except ValueError:
        return "BAD_SYNTAX"

    if src_port == 60788 and dst_port == 2901 and data_len == 28:
        return "TAK"
    else:
        return "NIE"

serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer...")

while True:
    dane, adres = serwer.recvfrom(1024)
    tekst = dane.decode().strip()

    print("Odebrano od", adres, ":", tekst)

    odpowiedz = check_msg_syntax(tekst)
    serwer.sendto(odpowiedz.encode(), adres)
```

---

10. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego wiadomość o treści podanej w zadaniu nr 14 z laboratorium nr 3, a następnie odeśle klientowi odpowiedź TAK lub NIE. W przypadku błędnego sformatowania wiadomości, serwer odeśle klientowi odpowiedź BAD SYNTAX.

```python
import socket

HOST = "127.0.0.1"
PORT = 2910

def check_msg_syntax(txt):
    parts = txt.split(";")

    if len(parts) != 7:
        return "BAD_SYNTAX"

    if parts[0] != "zad14odp" or parts[1] != "src" or parts[3] != "dst" or parts[5] != "data":
        return "BAD_SYNTAX"

    try:
        src_port = int(parts[2])
        dst_port = int(parts[4])
        data = parts[6]
    except ValueError:
        return "BAD_SYNTAX"

    if src_port == 2900 and dst_port == 35211 and data == "hello :)":
        return "TAK"
    else:
        return "NIE"

serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer...")

while True:
    dane, adres = serwer.recvfrom(1024)
    tekst = dane.decode().strip()

    print("Odebrano od", adres, ":", tekst)

    odpowiedz = check_msg_syntax(tekst)
    serwer.sendto(odpowiedz.encode(), adres)
```

---

11. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego wiadomość o treści podanej w zadaniu nr 15 z laboratorium nr 3, a następnie odeśle klientowi odpowiedź TAK lub NIE. W przypadku błędnego sformatowania wiadomości, serwer odeśle klientowi odpowiedź BAD SYNTAX.

```python
import socket

HOST = "127.0.0.1"
PORT = 2911

def check_msgA_syntax(txt):
    parts = txt.split(";")

    if len(parts) != 9:
        return "BAD_SYNTAX"

    if parts[0] != "zad15odpA" or parts[1] != "ver" or parts[3] != "srcip" or parts[5] != "dstip" or parts[7] != "type":
        return "BAD_SYNTAX"

    try:
        ver = int(parts[2])
        srcip = parts[4]
        dstip = parts[6]
        typ = int(parts[8])
    except ValueError:
        return "BAD_SYNTAX"

    if ver == 4 and typ == 6 and srcip == "212.182.24.27" and dstip == "192.168.0.2":
        return "TAK"
    else:
        return "NIE"


def check_msgB_syntax(txt):
    parts = txt.split(";")

    if len(parts) != 7:
        return "BAD_SYNTAX"

    if parts[0] != "zad15odpB" or parts[1] != "srcport" or parts[3] != "dstport" or parts[5] != "data":
        return "BAD_SYNTAX"

    try:
        srcport = int(parts[2])
        dstport = int(parts[4])
        data = parts[6]
    except ValueError:
        return "BAD_SYNTAX"

    if srcport == 2900 and dstport == 47526 and data == "network programming is fun":
        return "TAK"
    else:
        return "NIE"


serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer...")

while True:
    dane, adres = serwer.recvfrom(1024)
    tekst = dane.decode().strip()

    print("Odebrano od", adres, ":", tekst)

    parts = tekst.split(";")

    if not parts:
        odpowiedz = "BAD_SYNTAX"
    elif parts[0] == "zad15odpA":
        odpowiedz = check_msgA_syntax(tekst)
    elif parts[0] == "zad15odpB":
        odpowiedz = check_msgB_syntax(tekst)
    else:
        odpowiedz = "BAD_SYNTAX"

    serwer.sendto(odpowiedz.encode(), adres)
```