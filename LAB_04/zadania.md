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

---

7. Zmodyfikuj program nr 2 z laboratorium nr 3 w ten sposób, aby serwer wysyłał i odbierał wiadomość o maksymalnej długości 20 znaków.

---

8. Zmodyfikuj program nr 7 z laboratorium nr 3 w ten sposób, aby mieć pewność, że serwer w rzeczywistości odebrał / wysłał wiadomość o wymaganej długości.

---

9. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego wiadomość o treści podanej w zadaniu nr 13 z laboratorium nr 3, a następnie odeśle klientowi odpowiedź TAK lub NIE. W przypadku błędnego sformatowania wiadomości, serwer odeśle klientowi odpowiedź BAD SYNTAX.

---

10. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego wiadomość o treści podanej w zadaniu nr 14 z laboratorium nr 3, a następnie odeśle klientowi odpowiedź TAK lub NIE. W przypadku błędnego sformatowania wiadomości, serwer odeśle klientowi odpowiedź BAD SYNTAX.

---

11. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego wiadomość o treści podanej w zadaniu nr 15 z laboratorium nr 3, a następnie odeśle klientowi odpowiedź TAK lub NIE. W przypadku błędnego sformatowania wiadomości, serwer odeśle klientowi odpowiedź BAD SYNTAX.