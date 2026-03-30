> <u>Uwaga</u> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

---

1. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość e-mail używając komend protokołu ESMTP.

---

2. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość e-mail do kilku odbiorców używając komend protokołu ESMTP.

---

3. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość spoofed email (z podmienionym adresem nadawcy) używając komend protokołu ESMTP.

---

4. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny plik tekstowy (sprawdź format MIME: Multipart i Content-Type). Możesz wykorzystać openssl do przekonwertowania pliku: cat plik | openssl base64.

---

5. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem interia.pl na porcie 587 wyślij wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny obrazek (sprawdź format MIME: Multipart i Content-Type). Możesz wykorzystać openssl do przekonwertowania obrazka: cat obrazek |openssl base64.

---

6. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem interia.pl na porcie 587, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

---

7. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem interia.pl na porcie 587, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny plik tekstowy (sprawdź format MIME: Multipart i Content-Type). Nie wykorzystuj gotowych bibliotek. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

---

8. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem interia.pl na porcie 587, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny obrazek (sprawdź format MIME: Multipart i Content-Type). Nie wykorzystuj gotowych bibliotek. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

---

9. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem interia.pl na porcie 587, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Treść wiadomości powinna zostać sformatowana za pomocą tagów HTML, przykładowo: \<b><b>pogrubienie</b>\</b>, \<i><i>pochylenie</i>\</i>, \<u><u>podkreślenie</u>\</u> i innych wybranych.

---

10. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół SMTP. Nie realizuj faktycznego wysyłania e-maila, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient SMTP myślał, że wiadomość została wysłana. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.