> <u>Uwaga</u> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

---

1. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość e-mail używając komend protokołu ESMTP.

    1. Uruchomienie połączenia.

    Serwer wymaga STARTTLS, mimo że instrukcja pokazuje działający przykład z telnetem.

    ```bash
    openssl s_client -starttls smtp -connect poczta.interia.pl:587 -crlf
    ```

    Wyświetla się sporo informacji o TLS i na końcu baner serwera.

    2. Lista możliwości serwera

    ```bash
    EHLO test
    ```

    3. Logowanie

    * AUTH LOGIN
    * odpowiedź: 334 VXNlcm5hbWU6
    * kodowanie loginu w base64: python3 -c 'import base64; print(base64.b64encode("twoj_login@interia.pl".encode()).decode())'
    * kodowanie hasła: python3 -c 'import base64; print(base64.b64encode("twoje_haslo".encode()).decode())'
    * odpowiedź: 235 2.7.0 Authentication successful

    4. Podanie nadawcy

    ```bash
    MAIL FROM:<twoj_login@interia.pl>
    ```

    odpowiedź: `250 2.1.0 Ok`

    5. Podanie odbiorcy

    ```bash
    RCPT TO:<adres_odbiorcy@example.com>
    ```

    odpowiedź: `250 2.1.5 Ok`

    6. Treść wiadomości

    ```bash
    DATA
    ```

    odpowiedź: 354 End data with <CR><LF>.<CR><LF>

    Nagłówki:

    ```bash
    To: <adres_odbiorcy@example.com>
    From: <twoj_login@interia.pl>
    Subject: Test z laboratorium

    To jest testowa wiadomosc wyslana z terminala.
    .
    ```

    7. Zamknięcie połączenia

    ```bash
    QUIT
    ```

    odpowiedź: `221 2.0.0 Bye`

---

2. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość e-mail do kilku odbiorców używając komend protokołu ESMTP.

    1. Uruchomienie połączenia.

    Serwer wymaga STARTTLS, mimo że instrukcja pokazuje działający przykład z telnetem.

    ```bash
    openssl s_client -starttls smtp -connect poczta.interia.pl:587 -crlf
    ```

    Wyświetla się sporo informacji o TLS i na końcu baner serwera.

    2. Lista możliwości serwera

    ```bash
    EHLO test
    ```

    3. Logowanie

    * `AUTH LOGIN`
    * odpowiedź: `334 VXNlcm5hbWU6`
    * kodowanie loginu w base64:

        ```bash
        python3 -c 'import base64; print(base64.b64encode("twoj_login@interia.pl".encode()).decode())'
        ```
    * kodowanie hasła:

        ```bash
        python3 -c 'import base64; print(base64.b64encode("twoje_haslo".encode()).decode())'
        ```
    * odpowiedź: `235 2.7.0 Authentication successful`

    4. Podanie nadawcy

    ```bash
    MAIL FROM:<twoj_login@interia.pl>
    ```

    odpowiedź: `250 2.1.0 Ok`

    5. Podanie kilku odbiorców

    Dla każdego odbiorcy wpisujemy osobną komendę `RCPT TO`. Taki sposób wysyłki do kilku adresatów jest pokazany w materiałach. 

    ```bash
    RCPT TO:<odbiorca1@example.com>
    RCPT TO:<odbiorca2@example.com>
    RCPT TO:<odbiorca3@example.com>
    ```

    odpowiedź po każdej komendzie: `250 2.1.5 Ok`

    6. Treść wiadomości

    ```bash
    DATA
    ```

    odpowiedź: `354 End data with <CR><LF>.<CR><LF>`

    Nagłówki:

    ```bash
    To: <odbiorca1@example.com>, <odbiorca2@example.com>, <odbiorca3@example.com>
    From: <twoj_login@interia.pl>
    Subject: Test z laboratorium

    To jest testowa wiadomosc wyslana do kilku odbiorcow.
    .
    ```

    7. Zamknięcie połączenia

    ```bash
    QUIT
    ```

    odpowiedź: `221 2.0.0 Bye`

---

3. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość spoofed email (z podmienionym adresem nadawcy) używając komend protokołu ESMTP.

    1. połączenie z serwerem,
    2. EHLO,
    3. AUTH LOGIN,
    4. login i hasło w Base64,
    5. MAIL FROM,
    6. RCPT TO,
    7. DATA,
    8. nagłówki i treść,
    9. QUIT.

**Zmiana**:

W tym zadaniu zmieniamy pole nadawcy w nagłówku wiadomości. Na etapie DATA zamiast zwykłego:

```
To: <adres_odbiorcy@example.com>
From: <twoj_login@interia.pl>
Subject: Test z laboratorium

To jest testowa wiadomosc wyslana z terminala.
.
```

wpisujemy nagłówki z podmienionym polem From:, na przykład:

```
To: <adres_odbiorcy@example.com>
From: <inny_nadawca@example.com>
Subject: Test spoofed email

To jest testowa wiadomosc z podmienionym adresem nadawcy.
.
```

---

4. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny plik tekstowy (sprawdź format MIME: Multipart i Content-Type). Możesz wykorzystać openssl do przekonwertowania pliku: cat plik | openssl base64.

    1. Uruchomienie połączenia.

    Serwer wymaga STARTTLS, mimo że instrukcja pokazuje działający przykład z telnetem.

    ```bash
    openssl s_client -starttls smtp -connect poczta.interia.pl:587 -crlf
    ```

    Wyświetla się sporo informacji o TLS i na końcu baner serwera.

    2. Lista możliwości serwera

    ```bash
    EHLO test
    ```

    3. Logowanie

    * AUTH LOGIN
    * odpowiedź: 334 VXNlcm5hbWU6
    * kodowanie loginu w base64: `python3 -c 'import base64; print(base64.b64encode("twoj_login@interia.pl".encode()).decode())'`
    * kodowanie hasła: `python3 -c 'import base64; print(base64.b64encode("twoje_haslo".encode()).decode())'`
    * odpowiedź: 235 2.7.0 Authentication successful

    4. Podanie nadawcy

    ```bash
    MAIL FROM:<twoj_login@interia.pl>
    ```

    odpowiedź: 250 2.1.0 Ok

    5. Podanie odbiorcy

    ```bash
    RCPT TO:<adres_odbiorcy@example.com>
    ```

    odpowiedź: 250 2.1.5 Ok

    6. Przygotowanie załącznika

    Najpierw trzeba zakodować plik tekstowy do base64. Można to zrobić poleceniem:

    ```bash
    cat plik.txt | openssl base64
    ```

    Otrzymany wynik kopiujemy i wstawiamy później do treści wiadomości jako zawartość załącznika. Zadanie 4 i przykład z PDF-a dokładnie pokazują taki sposób przygotowania załącznika tekstowego w MIME.

    7. Treść wiadomości

    ```bash
    DATA
    ```

    odpowiedź: 354 End data with <CR><LF>.<CR><LF>

    Nagłówki i treść wiadomości z MIME:

    ```bash
    To: <adres_odbiorcy@example.com>
    From: <twoj_login@interia.pl>
    Subject: Test z laboratorium
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary=sep

    --sep
    To jest testowa wiadomosc z zalacznikiem.

    --sep
    Content-Type: text/plain; name="plik.txt"
    Content-Disposition: attachment; filename="plik.txt"
    Content-Transfer-Encoding: base64

    TU_WKLEJ_ZAWARTOSC_PLIKU_ZAKODOWANA_W_BASE64

    --sep--
    .
    ```

    8. Zamknięcie połączenia

    ```bash
    QUIT
    ```

    odpowiedź: 221 2.0.0 Bye

---

5. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny obrazek (sprawdź format MIME: Multipart i Content-Type). Możesz wykorzystać openssl do przekonwertowania obrazka: cat obrazek |openssl base64.

    1. Uruchomienie połączenia.

    Serwer wymaga STARTTLS, mimo że instrukcja pokazuje działający przykład z telnetem.

    ```bash
    openssl s_client -starttls smtp -connect poczta.interia.pl:587 -crlf
    ```

    Wyświetla się sporo informacji o TLS i na końcu baner serwera.

    2. Lista możliwości serwera

    ```bash
    EHLO test
    ```

    3. Logowanie

    * AUTH LOGIN
    * odpowiedź: 334 VXNlcm5hbWU6
    * kodowanie loginu w base64: `python3 -c 'import base64; print(base64.b64encode("twoj_login@interia.pl".encode()).decode())'`
    * kodowanie hasła: `python3 -c 'import base64; print(base64.b64encode("twoje_haslo".encode()).decode())'`
    * odpowiedź: 235 2.7.0 Authentication successful

    4. Podanie nadawcy

    ```bash
    MAIL FROM:<twoj_login@interia.pl>
    ```

    odpowiedź: 250 2.1.0 Ok

    5. Podanie odbiorcy

    ```bash
    RCPT TO:<adres_odbiorcy@example.com>
    ```

    odpowiedź: 250 2.1.5 Ok

    6. Przygotowanie załącznika

    Najpierw trzeba zakodować obrazek do base64. Można to zrobić poleceniem:

    ```bash
    cat obrazek.png | openssl base64
    ```

    Otrzymany wynik kopiujemy i wstawiamy później do treści wiadomości jako zawartość załącznika. W materiałach jest pokazane, że przy załącznikach trzeba użyć formatu MIME `multipart/mixed`, ustawić własny `boundary`, a sam załącznik przesłać z `Content-Transfer-Encoding: base64`. 

    7. Treść wiadomości

    ```bash
    DATA
    ```

    odpowiedź: 354 End data with <CR><LF>.<CR><LF>

    Nagłówki i treść wiadomości z MIME:

    ```bash
    To: <adres_odbiorcy@example.com>
    From: <twoj_login@interia.pl>
    Subject: Test z laboratorium
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary=sep

    --sep
    To jest testowa wiadomosc z zalacznikiem graficznym.

    --sep
    Content-Type: image/png; name="obrazek.png"
    Content-Disposition: attachment; filename="obrazek.png"
    Content-Transfer-Encoding: base64

    TU_WKLEJ_ZAWARTOSC_OBRAZKA_ZAKODOWANA_W_BASE64

    --sep--
    .
    ```

    Jeśli używasz pliku JPG, to zamiast `image/png` wpisujesz na przykład:

    ```bash
    Content-Type: image/jpeg; name="obrazek.jpg"
    ```

    8. Zamknięcie połączenia

    ```bash
    QUIT
    ```

    odpowiedź: 221 2.0.0 Bye

    W tym zadaniu do wiadomości został dodany załącznik graficzny przy użyciu formatu MIME. Wiadomość została przygotowana jako `multipart/mixed`, a obrazek został zakodowany w Base64. Do opisania załącznika użyto nagłówków `Content-Type`, `Content-Disposition` oraz `Content-Transfer-Encoding: base64`, zgodnie z zasadami MIME opisanymi w materiałach.

---

6. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem interia.pl na porcie 587, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

```python
import socket
import ssl
import base64

HOST = "poczta.interia.pl"
PORT = 587

def odbierz(sock):
    dane = b""
    while True:
        fragment = sock.recv(1024)
        dane += fragment
        if len(fragment) < 1024:
            break
    odpowiedz = dane.decode(errors="ignore")
    print(odpowiedz)
    return odpowiedz

def wyslij(sock, komenda):
    print(">>>", komenda.strip())
    sock.sendall(komenda.encode())
    return odbierz(sock)

def base64_encode(tekst):
    return base64.b64encode(tekst.encode()).decode()

nadawca = input("Podaj adres nadawcy: ").strip()
haslo = input("Podaj hasło: ").strip()
odbiorcy_tekst = input("Podaj odbiorców po przecinku: ").strip()
temat = input("Podaj temat: ").strip()

print("Podaj treść wiadomości. Zakończ wpisywanie pojedynczą kropką w osobnej linii:")
linie = []
while True:
    linia = input()
    if linia == ".":
        break
    linie.append(linia)

tresc = "\r\n".join(linie)
odbiorcy = [o.strip() for o in odbiorcy_tekst.split(",") if o.strip()]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

odbierz(sock)

wyslij(sock, "EHLO test\r\n")
wyslij(sock, "STARTTLS\r\n")

context = ssl.create_default_context()
sock = context.wrap_socket(sock, server_hostname=HOST)

wyslij(sock, "EHLO test\r\n")
wyslij(sock, "AUTH LOGIN\r\n")
wyslij(sock, base64_encode(nadawca) + "\r\n")
wyslij(sock, base64_encode(haslo) + "\r\n")

wyslij(sock, f"MAIL FROM:<{nadawca}>\r\n")

for odbiorca in odbiorcy:
    wyslij(sock, f"RCPT TO:<{odbiorca}>\r\n")

wyslij(sock, "DATA\r\n")

wiadomosc = (
    f"To: {', '.join(odbiorcy)}\r\n"
    f"From: {nadawca}\r\n"
    f"Subject: {temat}\r\n"
    "\r\n"
    f"{tresc}\r\n"
    ".\r\n"
)

print(">>> [treść wiadomości]")
sock.sendall(wiadomosc.encode())
odbierz(sock)

wyslij(sock, "QUIT\r\n")
sock.close()
```

---

7. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem interia.pl na porcie 587, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny plik tekstowy (sprawdź format MIME: Multipart i Content-Type). Nie wykorzystuj gotowych bibliotek. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

```python
import socket
import ssl
import base64
import os

HOST = "poczta.interia.pl"
PORT = 587

def odbierz(sock):
    dane = b""
    while True:
        fragment = sock.recv(1024)
        dane += fragment
        if len(fragment) < 1024:
            break
    odpowiedz = dane.decode(errors="ignore")
    print(odpowiedz)
    return odpowiedz

def wyslij(sock, komenda):
    print(">>>", komenda.strip())
    sock.sendall(komenda.encode())
    return odbierz(sock)

def koduj_base64_tekst(tekst):
    return base64.b64encode(tekst.encode()).decode()

def koduj_base64_plik(sciezka):
    with open(sciezka, "rb") as plik:
        return base64.b64encode(plik.read()).decode()

nadawca = input("Podaj adres nadawcy: ").strip()
haslo = input("Podaj hasło: ").strip()
odbiorcy_tekst = input("Podaj odbiorców po przecinku: ").strip()
temat = input("Podaj temat wiadomości: ").strip()

print("Podaj treść wiadomości. Zakończ pojedynczą kropką w osobnej linii:")
linie = []
while True:
    linia = input()
    if linia == ".":
        break
    linie.append(linia)

tresc = "\r\n".join(linie)

sciezka_pliku = input("Podaj ścieżkę do pliku tekstowego: ").strip()
nazwa_pliku = os.path.basename(sciezka_pliku)

odbiorcy = [o.strip() for o in odbiorcy_tekst.split(",") if o.strip()]
zalacznik_base64 = koduj_base64_plik(sciezka_pliku)

boundary = "sep"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

odbierz(sock)

wyslij(sock, "EHLO test\r\n")
wyslij(sock, "STARTTLS\r\n")

context = ssl.create_default_context()
sock = context.wrap_socket(sock, server_hostname=HOST)

wyslij(sock, "EHLO test\r\n")
wyslij(sock, "AUTH LOGIN\r\n")
wyslij(sock, koduj_base64_tekst(nadawca) + "\r\n")
wyslij(sock, koduj_base64_tekst(haslo) + "\r\n")

wyslij(sock, f"MAIL FROM:<{nadawca}>\r\n")

for odbiorca in odbiorcy:
    wyslij(sock, f"RCPT TO:<{odbiorca}>\r\n")

wyslij(sock, "DATA\r\n")

wiadomosc = (
    f"To: {', '.join(odbiorcy)}\r\n"
    f"From: {nadawca}\r\n"
    f"Subject: {temat}\r\n"
    f"MIME-Version: 1.0\r\n"
    f"Content-Type: multipart/mixed; boundary={boundary}\r\n"
    f"\r\n"
    f"--{boundary}\r\n"
    f"{tresc}\r\n"
    f"\r\n"
    f"--{boundary}\r\n"
    f"Content-Type: text/plain; name=\"{nazwa_pliku}\"\r\n"
    f"Content-Disposition: attachment; filename=\"{nazwa_pliku}\"\r\n"
    f"Content-Transfer-Encoding: base64\r\n"
    f"\r\n"
    f"{zalacznik_base64}\r\n"
    f"--{boundary}--\r\n"
    f".\r\n"
)

print(">>> [wysyłanie wiadomości MIME z załącznikiem]")
sock.sendall(wiadomosc.encode())
odbierz(sock)

wyslij(sock, "QUIT\r\n")
sock.close()
```

---

8. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem interia.pl na porcie 587, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny obrazek (sprawdź format MIME: Multipart i Content-Type). Nie wykorzystuj gotowych bibliotek. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

```python
import socket
import ssl
import base64
import os

HOST = "poczta.interia.pl"
PORT = 587

def odbierz(sock):
    dane = b""
    while True:
        fragment = sock.recv(1024)
        dane += fragment
        if len(fragment) < 1024:
            break
    odpowiedz = dane.decode(errors="ignore")
    print(odpowiedz)
    return odpowiedz

def wyslij(sock, komenda):
    print(">>>", komenda.strip())
    sock.sendall(komenda.encode())
    return odbierz(sock)

def koduj_base64_tekst(tekst):
    return base64.b64encode(tekst.encode()).decode()

def koduj_base64_plik(sciezka):
    with open(sciezka, "rb") as plik:
        return base64.b64encode(plik.read()).decode()

def typ_mime_obrazka(nazwa_pliku):
    nazwa = nazwa_pliku.lower()

    if nazwa.endswith(".png"):
        return "image/png"
    elif nazwa.endswith(".jpg") or nazwa.endswith(".jpeg"):
        return "image/jpeg"
    elif nazwa.endswith(".gif"):
        return "image/gif"
    elif nazwa.endswith(".bmp"):
        return "image/bmp"
    elif nazwa.endswith(".webp"):
        return "image/webp"
    else:
        return "application/octet-stream"

nadawca = input("Podaj adres nadawcy: ").strip()
haslo = input("Podaj hasło: ").strip()
odbiorcy_tekst = input("Podaj odbiorców po przecinku: ").strip()
temat = input("Podaj temat wiadomości: ").strip()

print("Podaj treść wiadomości. Zakończ pojedynczą kropką w osobnej linii:")
linie = []
while True:
    linia = input()
    if linia == ".":
        break
    linie.append(linia)

tresc = "\r\n".join(linie)

sciezka_pliku = input("Podaj ścieżkę do obrazka: ").strip()
nazwa_pliku = os.path.basename(sciezka_pliku)
mime_typ = typ_mime_obrazka(nazwa_pliku)

odbiorcy = [o.strip() for o in odbiorcy_tekst.split(",") if o.strip()]
zalacznik_base64 = koduj_base64_plik(sciezka_pliku)

boundary = "sep"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

odbierz(sock)

wyslij(sock, "EHLO test\r\n")
wyslij(sock, "STARTTLS\r\n")

context = ssl.create_default_context()
sock = context.wrap_socket(sock, server_hostname=HOST)

wyslij(sock, "EHLO test\r\n")
wyslij(sock, "AUTH LOGIN\r\n")
wyslij(sock, koduj_base64_tekst(nadawca) + "\r\n")
wyslij(sock, koduj_base64_tekst(haslo) + "\r\n")

wyslij(sock, f"MAIL FROM:<{nadawca}>\r\n")

for odbiorca in odbiorcy:
    wyslij(sock, f"RCPT TO:<{odbiorca}>\r\n")

wyslij(sock, "DATA\r\n")

wiadomosc = (
    f"To: {', '.join(odbiorcy)}\r\n"
    f"From: {nadawca}\r\n"
    f"Subject: {temat}\r\n"
    f"MIME-Version: 1.0\r\n"
    f"Content-Type: multipart/mixed; boundary={boundary}\r\n"
    f"\r\n"
    f"--{boundary}\r\n"
    f"Content-Type: text/plain; charset=utf-8\r\n"
    f"\r\n"
    f"{tresc}\r\n"
    f"\r\n"
    f"--{boundary}\r\n"
    f"Content-Type: {mime_typ}; name=\"{nazwa_pliku}\"\r\n"
    f"Content-Disposition: attachment; filename=\"{nazwa_pliku}\"\r\n"
    f"Content-Transfer-Encoding: base64\r\n"
    f"\r\n"
    f"{zalacznik_base64}\r\n"
    f"--{boundary}--\r\n"
    f".\r\n"
)

print(">>> [wysyłanie wiadomości MIME z obrazkiem]")
sock.sendall(wiadomosc.encode())
odbierz(sock)

wyslij(sock, "QUIT\r\n")
sock.close()
```

---

9. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem interia.pl na porcie 587, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Treść wiadomości powinna zostać sformatowana za pomocą tagów HTML, przykładowo: \<b><b>pogrubienie</b>\</b>, \<i><i>pochylenie</i>\</i>, \<u><u>podkreślenie</u>\</u> i innych wybranych.

```python
import socket
import ssl
import base64

HOST = "poczta.interia.pl"
PORT = 587

def odbierz(sock):
    dane = b""
    while True:
        fragment = sock.recv(1024)
        dane += fragment
        if len(fragment) < 1024:
            break
    odpowiedz = dane.decode(errors="ignore")
    print(odpowiedz)
    return odpowiedz

def wyslij(sock, komenda):
    print(">>>", komenda.strip())
    sock.sendall(komenda.encode())
    return odbierz(sock)

def koduj_base64(tekst):
    return base64.b64encode(tekst.encode()).decode()

nadawca = input("Podaj adres nadawcy: ").strip()
haslo = input("Podaj hasło: ").strip()
odbiorcy_tekst = input("Podaj odbiorców po przecinku: ").strip()
temat = input("Podaj temat wiadomości: ").strip()

print("Podaj treść HTML wiadomości. Zakończ pojedynczą kropką w osobnej linii:")
linie = []
while True:
    linia = input()
    if linia == ".":
        break
    linie.append(linia)

tresc_html = "\r\n".join(linie)
odbiorcy = [o.strip() for o in odbiorcy_tekst.split(",") if o.strip()]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

odbierz(sock)

wyslij(sock, "EHLO test\r\n")
wyslij(sock, "STARTTLS\r\n")

context = ssl.create_default_context()
sock = context.wrap_socket(sock, server_hostname=HOST)

wyslij(sock, "EHLO test\r\n")
wyslij(sock, "AUTH LOGIN\r\n")
wyslij(sock, koduj_base64(nadawca) + "\r\n")
wyslij(sock, koduj_base64(haslo) + "\r\n")

wyslij(sock, f"MAIL FROM:<{nadawca}>\r\n")

for odbiorca in odbiorcy:
    wyslij(sock, f"RCPT TO:<{odbiorca}>\r\n")

wyslij(sock, "DATA\r\n")

wiadomosc = (
    f"To: {', '.join(odbiorcy)}\r\n"
    f"From: {nadawca}\r\n"
    f"Subject: {temat}\r\n"
    f"MIME-Version: 1.0\r\n"
    f"Content-Type: text/html; charset=utf-8\r\n"
    f"\r\n"
    f"{tresc_html}\r\n"
    f".\r\n"
)

print(">>> [wysyłanie wiadomości HTML]")
sock.sendall(wiadomosc.encode("utf-8"))
odbierz(sock)

wyslij(sock, "QUIT\r\n")
sock.close()
```

Przykładowa treść:

```html
<html>
<body>
<h2>Test wiadomości HTML</h2>
<p>To jest <b>pogrubienie</b>, <i>pochylenie</i> oraz <u>podkreślenie</u>.</p>
<p style="color: red;">To jest czerwony tekst.</p>
</body>
</html>
.
```

---

10. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół SMTP. Nie realizuj faktycznego wysyłania e-maila, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient SMTP myślał, że wiadomość została wysłana. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.

```python
import socket
import ssl
import base64

HOST = "127.0.0.1"
PORT = 2525

CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"


def wyslij_linie(polaczenie, tekst):
    polaczenie.sendall((tekst + "\r\n").encode())


def odbierz_linie(plik):
    linia = plik.readline()
    if not linia:
        return None
    return linia.decode(errors="ignore").rstrip("\r\n")


serwer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serwer.bind((HOST, PORT))
serwer.listen(1)

print(f"Serwer SMTP działa na {HOST}:{PORT}")

while True:
    klient, adres = serwer.accept()
    print("Połączono z:", adres)

    plik = klient.makefile("rb")

    tls_aktywne = False
    zalogowany = False
    mail_from = None
    rcpt_to = []
    tresc_wiadomosci = []

    wyslij_linie(klient, "220 localhost SMTP ready")

    while True:
        linia = odbierz_linie(plik)

        if linia is None:
            break

        print("C:", linia)

        if linia.upper().startswith("HELO"):
            wyslij_linie(klient, "250 localhost")

        elif linia.upper().startswith("HELO"):
            wyslij_linie(klient, "250-localhost")
            wyslij_linie(klient, "250-STARTTLS")
            wyslij_linie(klient, "250-AUTH LOGIN")
            wyslij_linie(klient, "250 OK")

        elif linia.upper() == "STARTTLS":
            wyslij_linie(klient, "220 Ready to start TLS")

            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

            klient = context.wrap_socket(klient, server_side=True)
            plik = klient.makefile("rb")
            tls_aktywne = True

        elif linia.upper() == "AUTH LOGIN":
            wyslij_linie(klient, "334 VXNlcm5hbWU6")  # Username:
            login_b64 = odbierz_linie(plik)
            print("C:", login_b64)

            wyslij_linie(klient, "334 UGFzc3dvcmQ6")  # Password:
            haslo_b64 = odbierz_linie(plik)
            print("C:", haslo_b64)

            # tylko dla podglądu – nie trzeba tego nawet sprawdzać
            try:
                login = base64.b64decode(login_b64).decode(errors="ignore")
                haslo = base64.b64decode(haslo_b64).decode(errors="ignore")
                print("Login:", login)
                print("Hasło:", haslo)
            except:
                pass

            zalogowany = True
            wyslij_linie(klient, "235 2.7.0 Authentication successful")

        elif linia.upper().startswith("MAIL FROM:"):
            if not zalogowany:
                wyslij_linie(klient, "530 5.7.0 Authentication required")
            else:
                mail_from = linia[10:].strip()
                wyslij_linie(klient, "250 2.1.0 Ok")

        elif linia.upper().startswith("RCPT TO:"):
            if mail_from is None:
                wyslij_linie(klient, "503 5.5.1 Need MAIL FROM first")
            else:
                rcpt_to.append(linia[8:].strip())
                wyslij_linie(klient, "250 2.1.5 Ok")

        elif linia.upper() == "DATA":
            if not rcpt_to:
                wyslij_linie(klient, "503 5.5.1 Need RCPT TO first")
            else:
                wyslij_linie(klient, "354 End data with <CR><LF>.<CR><LF>")

                tresc_wiadomosci = []
                while True:
                    wiersz = odbierz_linie(plik)
                    if wiersz == ".":
                        break
                    tresc_wiadomosci.append(wiersz)

                print("=== ODEBRANA WIADOMOŚĆ ===")
                print("MAIL FROM:", mail_from)
                print("RCPT TO:", rcpt_to)
                print("\n".join(tresc_wiadomosci))
                print("==========================")

                wyslij_linie(klient, "250 2.0.0 OK: message accepted")

                # reset danych do następnej wiadomości
                mail_from = None
                rcpt_to = []
                tresc_wiadomosci = []

        elif linia.upper() == "RSET":
            mail_from = None
            rcpt_to = []
            tresc_wiadomosci = []
            wyslij_linie(klient, "250 Ok")

        elif linia.upper() == "NOOP":
            wyslij_linie(klient, "250 Ok")

        elif linia.upper() == "QUIT":
            wyslij_linie(klient, "221 2.0.0 Bye")
            break

        else:
            wyslij_linie(klient, "500 5.5.2 Command not recognized")

    klient.close()
```

## Jak to przetestować

### 1. Wygeneruj lokalny certyfikat

Bo serwer obsługuje `STARTTLS`.

W terminalu Linux:

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
```

To utworzy pliki:

* `cert.pem`
* `key.pem`

Muszą leżeć w tym samym katalogu co serwer.

---

### 2. Uruchom serwer

```bash
python3 serwer_smtp.py
```

---

### 3. Podłącz klienta

Możesz testować:

* swoim wcześniejszym klientem w Pythonie,
* albo ręcznie przez:

```bash
openssl s_client -starttls smtp -connect 127.0.0.1:2525 -crlf
```