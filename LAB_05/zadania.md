> <u>Uwaga:</u> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili

---

1. Pod adresem 212.182.24.27 na porcie TCP o numerze 2912 działa serwer losujący liczby. Napisz program klienta, który będzie pobierał od użytkownika liczbę, a następnie będzie wysyłał ją do serwera w celu odgadnięcia wylosowanej przez serwer liczby. Po wysłaniu liczby klient powienien odbierać od serwera odpowiedź mówiącą o tym, czy udało nam się daną liczbę odgadnąć.

```python
import socket

HOST = "127.0.0.1"
PORT = 2912

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    user_input = input("Zakończ działanie programu za pomocą q lub podaj liczbę: ")

    if user_input.lower() == 'q':
        break

    sock.send(user_input.encode())

    odpowiedz = sock.recv(1024).decode()
    print("Odpowiedź serwera:", odpowiedz)

    if "correct" in odpowiedz.lower() or "poprawna" in odpowiedz.lower() or "brawo" in odpowiedz.lower():
        break

sock.close()
```

---

2. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP będzie losował liczbę i odbierał od klienta wiadomości. W przypadku, gdy w wiadomości klient przyśle do serwera coś innego, niż liczbę, serwer powinien poinformować klienta o błędzie. Po odebraniu liczby od klienta, serwer sprawdza, czy otrzymana liczba jest:

- mniejsza od wylosowanej przez serwer
- równa wylosowanej przez serwer
- większa od wylosowanej przez serwer

A następnie odsyła stosowną informację do klienta. W przypadku, gdy klient odgadnie liczbę, serwer powinien zakończyć działanie.

```python
import socket
import random

HOST = "127.0.0.1"
PORT = 2912

wylosowana_liczba = random.randint(1, 100)
print("Wylosowana liczba:", wylosowana_liczba)

serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serwer.bind((HOST, PORT))
serwer.listen(1)

print("Uruchomiono serwer...")

klient, adres = serwer.accept()
print("Połączono")

while True:
    dane = klient.recv(1024)

    if not dane:
        break

    tekst = dane.decode().strip()

    try:
        liczba = int(tekst)
    except ValueError:
        klient.send("Proszę podać liczbę".encode())
        continue

    if liczba < wylosowana_liczba:
        klient.send("Za mała".encode())
    elif liczba > wylosowana_liczba:
        klient.send("Za duża".encode())
    else:
        klient.send("Brawo, odgadnięto liczbę".encode())
        break

klient.close()
serwer.close()
```

---

3. <b>Port-knocking</b> jest metodą pozwalającą na nawiązanie zdalnego połączenia z usługami działającymi na komputerze, do którego dostęp został ograniczony np. za pomocą zapory sieciowej, umożliwiającą odróżniania prób połączeń, które powinny i nie powinny być zrealizowane. Inaczej mówiąc, to metoda ustanawiania połączenia z hostem o zamkniętych portach.

Pod adresem 212.182.24.27 na porcie TCP o numerze 2913 działa ukryta usługa. Usługa jest zabezpieczona metodą port knocking - po otrzymaniu od klienta odpowiedniej sekwencji pakietów UDP na odpowiednie porty, otwiera wspomniany wyżej port TCP. Napisz program klienta, który odgadnie sekwencję portów UDP, a następnie odbierze od serwera wiadomość na porcie TCP.

<u>Uwaga:</u> Aby znaleźć porty UDP, składające się na sekwencję otwarcia docelowego portu TCP, wysyłaj do serwera wiadomość o treści PING. W przypadku, gdy uda się znaleźć port UDP, należący do sekwencji otwierającej port TCP, serwer odeśle wiadomość PONG. Porty UDP, które wchodzą w skład sekwencji kończą się na 666. Usługa działająca na ukrytym porcie, jeśli uda się ją znaleźć, zwraca w odpowiedzi tekst: <b>Congratulations! You found the hidden.</b>

```python
import socket
import time

HOST = "127.0.0.1"
TCP_PORT = 2913

znalezione_porty = []

for port in range(666, 65536, 1000):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.settimeout(0.5)

    try:
        udp.sendto(b"PING", (HOST, port))
        dane, _ = udp.recvfrom(1024)

        if dane.decode().strip() == "PONG":
            print("Znaleziono port sekwencji:", port)
            znalezione_porty.append(port)

    except:
        pass

    udp.close()
    time.sleep(0.05)

print("Znalezione porty:", znalezione_porty)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.settimeout(2)

try:
    tcp.connect((HOST, TCP_PORT))
    odpowiedz = tcp.recv(1024).decode()
    print("Ukryta usługa odpowiedziała:", odpowiedz)
except Exception as e:
    print("Nie udało się połączyć z ukrytą usługą:", e)

tcp.close()
```

---

4. Napisz parę programów - klienta i serwer, w których porównasz czas przesyłu pakietów za pomocą gniazda TCP i gniazda UDP. Następnie, po przeprowadzonym teście, odpowiedz na pytania:

- Dla którego z gniazd czas jest krótszy?
- Z czego wynika krótszy czas?
- Jakie są zalety / wady obu rozwiązań?

### TCP
Klient:

```python
import socket
import time

HOST = "127.0.0.1"
PORT = 5000
ROZMIAR = 60000

dane = b"A" * ROZMIAR

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

start = time.perf_counter()
sock.sendall(dane)

odebrane = 0
while odebrane < ROZMIAR:
    fragment = sock.recv(65535)
    if not fragment:
        break
    odebrane += len(fragment)

koniec = time.perf_counter()

print("TCP czas:", koniec - start, "s")
sock.close()
```

Serwer:

```python
import socket
import time

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serwer.bind((HOST, PORT))
serwer.listen(1)

print("Uruchomiono serwer TCP")

klient, adres = serwer.accept()

while True:
    dane = klient.recv(65535)
    if not dane:
        break
    klient.sendall(dane)

klient.close()
serwer.close()
```

### UDP
Klient:

```python
import socket
import time

HOST = "127.0.0.1"
PORT = 5000
ROZMIAR = 60000

dane = b"A" * ROZMIAR

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start = time.perf_counter()
sock.sendto(dane, (HOST, PORT))
odpowiedz, _ = sock.recvfrom(65535)
koniec = time.perf_counter()

print("UDP czas:", koniec - start, "s")
sock.close()
```

Serwer:

```python
import socket

HOST = "127.0.0.1"
PORT = 5000

serwer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serwer.bind((HOST, PORT))

print("Uruchomiono serwer UDP")

while True:
    dane, adres = serwer.recvfrom(65535)
    serwer.sendto(dane, adres)
```

#### Dla którego z gniazd czas jest krótszy?
`Krótszy czas przesyłu ma zwykle gniazdo UDP.`

#### Z czego wynika krótszy czas?
`Wynika to z tego, że UDP nie wymaga nawiązania połączenia między klientem a serwerem i ma mniejszy narzut niż TCP. Nie sprawdza też poprawności dostarczenia danych ani nie kontroluje kolejności pakietów, dlatego działa szybciej.`

#### Jakie są zalety / wady obu rozwiązań?
`TCP ma taką zaletę, że zapewnia pewne dostarczenie danych, zachowanie ich kolejności i większą niezawodność transmisji. Jego wadą jest większy narzut i wolniejsze działanie.`

`UDP ma taką zaletę, że jest szybsze i prostsze. Jego wadą jest brak gwarancji dostarczenia danych, brak kontroli kolejności pakietów i brak potwierdzenia odbioru.`