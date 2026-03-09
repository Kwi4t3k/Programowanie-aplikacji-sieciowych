1. Napisz program, który z serwera ntp.task.gda.pl pobierze aktualną datę i czas, a następnie wyświetli je
na konsoli. Serwer działa na porcie 13.

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("ntp.task.gda.pl", 13))

result = sock.recv(1024)
print(result.decode())

sock.close()
```

---

2. Napisz program klienta, który połączy się z serwerem TCP działającym pod adresem 212.182.24.27 na
porcie 2900, a następnie wyśle do niego wiadomość i odbierze odpowiedź.

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("212.182.24.27", 2900))
# sock.connect(("127.0.0.1", 2900)) # bo serwer z plików działa na localhost

message = input("Podaj wiadomość:")
sock.send(message.encode())
result = sock.recv(1024)
print(result.decode())

sock.close()
```

---

3. Napisz program klienta, który połączy się z serwerem TCP działającym pod adresem 212.182.24.27 na
porcie 2900, a następnie będzie w pętli wysyłał do niego tekst wczytany od użytkownika, i odbierał
odpowiedzi.

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("212.182.24.27", 2900))
# sock.connect(("127.0.0.1", 2900)) # bo serwer z plików działa na localhost

while 1:
    message = input("Podaj wiadomość:")
    sock.send(message.encode())
    result = sock.recv(1024)
    print(result.decode())

    if message == "stop":
        break

sock.close()
```

---

4. Napisz program klienta, który połączy się z serwerem UDP działającym pod adresem 212.182.24.27 na
porcie 2901, a następnie wyśle do niego wiadomość i odbierze odpowiedź.

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("212.182.24.27", 2901))
# sock.connect(("127.0.0.1", 2901))

message = input("Podaj wiadomość:")
sock.send(message.encode())
result = sock.recv(1024)
print(result.decode())

sock.close()
```

---

5. Napisz program klienta, który połączy się z serwerem UDP działającym pod adresem 212.182.24.27 na
porcie 2901, a następnie będzie w pętli wysyłał do niego tekst wczytany od użytkownika, i odbierał
odpowiedzi.

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("212.182.24.27", 2901))
# sock.connect(("127.0.0.1", 2901))

while 1:
    message = input("Podaj wiadomość:")
    sock.send(message.encode())
    result = sock.recv(1024)
    print(result.decode())

    if message == "stop":
        break

sock.close()
```

---

6. Napisz program klienta, który połączy się z serwerem UDP działającym pod adresem 212.182.24.27 na
porcie 2902, a następnie prześle do serwera liczbę, operator, liczbę (pobrane od użytkownika) i odbierze
odpowiedź.

```python

```

---

7. Zmodyfikuj program numer 6 z laboratorium nr 1 w ten sposób, aby oprócz wyświetlania informacji o
tym, czy port jest zamknięty, czy otwarty, klient wyświetlał również informację o tym, jaka usługa jest
uruchomiona na danym porcie.

```python

```

---

8. Zmodyfikuj program numer 7 z laboratorium nr 1 w ten sposób, aby oprócz wyświetlania informacji o
tym, czy porty są jest zamknięte, czy otwarte, klient wyświetlał również informację o tym, jaka usługa
jest uruchomiona na danym porcie.

```python

```

---

9. Napisz program klienta, który połączy się z serwerem UDP działającym pod adresem 212.182.24.27 na
porcie 2906, a następnie prześle do serwera adres IP, i odbierze odpowiadającą mu nazwę hostname.

```python

```

---

10. Napisz program klienta, który połączy się z serwerem UDP działającym pod adresem 212.182.24.27 na
porcie 2907, a następnie prześle do serwera nazwę hostname, i odbierze odpowiadający mu adres IP.

```python

```

---

11. Zmodyfikuj program nr 2 z laboratorium nr 2 w ten sposób, aby klient wysłał i odebrał od serwera wiadomość o maksymalnej długości 20 znaków. Serwer TCP odbierający i wysyłający wiadomości o długości
20 działa pod adresem 212.182.24.27 na porcie 2908. Uwzględnij sytuacje, gdy:

    • wiadomość do wysłania jest za krótka - ma być wówczas uzupełniania do 20 znaków znakami spacji

    • wiadomość do wysłania jest za długa - ma być przycięta do 20 znaków (lub wysłana w całości -
sprawdź, co się wówczas stanie)

```python

```

---

12. Funkcje recv i send nie gwarantują wysłania / odbioru wszystkich danych. Rozważmy funkcję recv.
Przykładowo, 100 bajtów może zostać wysłane jako grupa po 10 bajtów, albo od razu w całości. Oznacza
to, iż jeśli używamy gniazd TCP, musimy odbierać dane, dopóki nie mamy pewności, że odebraliśmy
odpowiednią ich ilość. Zmodyfikuj program nr 11 z laboratorium nr 2 w ten sposób, aby mieć pewność,
że klient w rzeczywistości odebrał / wysłał wiadomość o wymaganej długości.

```python

```