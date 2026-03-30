<b><u>Uwaga</u></b> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

---

1. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile wiadomości znajduje się w skrzynce.

---

2. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile bajtów (w sumie) zajmują wiadomości znajdujące się w skrzynce.

---

3. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile bajtów zajmuje każda wiadomość (z osobna) znajdująca się w skrzynce.

---

4. Wykorzystując protokół telnet, oraz wybrany serwer POP3, wyświetl treść wiadomości o największym rozmiarze.

---

5. Wykorzystując protokół telnet, oraz wybrany serwer POP3, usuń wiadomość o najmniejszym rozmiarze.

---

6. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile wiadomości znajduje się w skrzynce.

---

7. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile bajtów (w sumie) zajmują wiadomości znajdujące się w skrzynce.

---

8. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile bajtów zajmuje każda wiadomość (z osobna) znajdująca się w skrzynce.

---

9. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetl treść wiadomości o największym rozmiarze.

---

10. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli wszystkie wiadomości znajdujące się w skrzynce.

---

11. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie pobierze z serwera wiadomość z załącznikiem (obrazkiem) i zapisze obrazek na dysk. Nazwa obrazka musi zgadzać się z nazwą załącznika podaną w mailu. Pamiętaj, że do przesyłania załączników binarnych w poczcie elektronicznej wykorzystywane jest kodowanie Base64.

---

12. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół POP3. Nie realizuj faktycznego pobierania e-maili, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient POP3 mógł pobrac wiadomosci. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.