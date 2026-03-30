<b><u>Uwaga</u></b> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

---

1. Wykorzystując protokół telnet, oraz serwer IMAP, zaloguj się do skrzynki i sprawdź, ile wiadomości znajduje się w poszczególnych skrzynkach. Pobierz pierwszą dostępną wiadomość, i oznacz ją jako przeczytaną. Wykorzystaj komendę protokołu IMAP - STORE.

---

2. Napisz program klienta, który połączy się z serwerem IMAP, a następnie wyświetli informację o tym, ile wiadomości znajduje się w skrzynce Inbox.

---

3. Napisz program klienta, który połączy się z serwerem IMAP, a następnie wyświetli informację o tym, ile wiadomości znajduje się we wszystkich skrzynkach łącznie.

---

4. Napisz program klienta, który połączy się z serwerem IMAP, a następnie sprawdzi, czy w skrzynce są nieprzeczytane wiadomości. Jeśli tak, wyświetli treść wszystkich nieprzeczytanych wiadomości oraz oznaczy je jako przeczytane (komenda STORE i flagi - FLAGS).

---

5. Napisz program klienta, który połączy się z serwerem IMAP, a następnie fizycznie usunie wybraną wiadomość.

---

6. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół IMAP. Nie realizuj faktycznego pobierania e-maili, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient IMAP mógł pobrac wiadomosci. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.