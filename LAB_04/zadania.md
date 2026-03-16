> Uwaga! W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

---

1. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, dla podłączającego się klienta, będzie odsyłał mu aktualny czas oraz datę. Prawidłowa komunikacja powinna odbywać się w nastepujacy sposób:
- Serwer odbiera od klienta wiadomość (dowolną)
- Serwer odsyła klientowi aktualną datę i czas

---

2. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie TCP, dla podłączającego się klienta, będzie odsyłał mu przesłaną wiadomość (tzw. serwer echa). Prawidłowa komunikacja
powinna odbywać się w nastepujacy sposób:
- Serwer odbiera dane od klienta
- Serwer odsyła klientowi odebrane od niego dane

---

3. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, będzie odsyłał mu przesłaną wiadomość (tzw. serwer echa). Prawidłowa komunikacja powinna odbywać się w nastepujacy sposób:
- Serwer odbiera dane od klienta
- Serwer odsyła klientowi odebrane od niego dane

---

4. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, będzie odbierał liczbę, operator i liczbę, a następnie odsyłał użytkownikowi wynik działania, przez niego przesłanego.

---

5. Napisz program serwera, który działając pod adresem 127.0.0.1 oraz na określonym porcie UDP, dla podłączającego się klienta, odbierze od niego adres IP, i odeśle odpowiadającą mu nazwę hostname.

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