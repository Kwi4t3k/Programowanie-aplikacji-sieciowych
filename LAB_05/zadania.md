> <u>Uwaga:</u> W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili

---

1. Pod adresem 212.182.24.27 na porcie TCP o numerze 2912 działa serwer losujący liczby. Napisz program klienta, który będzie pobierał od użytkownika liczbę, a następnie będzie wysyłał ją do serwera w celu odgadnięcia wylosowanej przez serwer liczby. Po wysłaniu liczby klient powienien odbierać od serwera odpowiedź mówiącą o tym, czy udało nam się daną liczbę odgadnąć.

---

2. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP będzie losował liczbę i odbierał od klienta wiadomości. W przypadku, gdy w wiadomości klient przyśle do serwera coś innego, niż liczbę, serwer powinien poinformować klienta o błędzie. Po odebraniu liczby od klienta, serwer sprawdza, czy otrzymana liczba jest:

- mniejsza od wylosowanej przez serwer
- równa wylosowanej przez serwer
- większa od wylosowanej przez serwer

A następnie odsyła stosowną informację do klienta. W przypadku, gdy klient odgadnie liczbę, serwer powinien zakończyć działanie.

---

3. <b>Port-knocking</b> jest metodą pozwalającą na nawiązanie zdalnego połączenia z usługami działającymi na komputerze, do którego dostęp został ograniczony np. za pomocą zapory sieciowej, umożliwiającą odróżniania prób połączeń, które powinny i nie powinny być zrealizowane. Inaczej mówiąc, to metoda ustanawiania połączenia z hostem o zamkniętych portach.

Pod adresem 212.182.24.27 na porcie TCP o numerze 2913 działa ukryta usługa. Usługa jest zabezpieczona metodą port knocking - po otrzymaniu od klienta odpowiedniej sekwencji pakietów UDP na odpowiednie porty, otwiera wspomniany wyżej port TCP. Napisz program klienta, który odgadnie sekwencję portów UDP, a następnie odbierze od serwera wiadomość na porcie TCP.

<u>Uwaga:</u> Aby znaleźć porty UDP, składające się na sekwencję otwarcia docelowego portu TCP, wysyłaj do serwera wiadomość o treści PING. W przypadku, gdy uda się znaleźć port UDP, należący do sekwencji otwierającej port TCP, serwer odeśle wiadomość PONG. Porty UDP, które wchodzą w skład sekwencji kończą się na 666. Usługa działająca na ukrytym porcie, jeśli uda się ją znaleźć, zwraca w odpowiedzi tekst: <b>Congratulations! You found the hidden.</b>

---

4. Napisz parę programów - klienta i serwer, w których porównasz czas przesyłu pakietów za pomocą gniazda TCP i gniazda UDP. Następnie, po przeprowadzonym teście, odpowiedz na pytania:

- Dla którego z gniazd czas jest krótszy?
- Z czego wynika krótszy czas?
- Jakie są zalety / wady obu rozwiązań?