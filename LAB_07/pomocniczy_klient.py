import socket

HOST = "interia.pl"   # albo 212.182.24.27
PORT = 110
USER = "twoj_login"
PASSWORD = "twoje_haslo"

class POP3Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.file = self.sock.makefile("rb")
        print(self._readline())

    def _readline(self):
        line = self.file.readline()
        if not line:
            raise ConnectionError("Połączenie zostało zamknięte")
        return line.decode(errors="ignore").rstrip("\r\n")

    def command(self, cmd):
        self.sock.sendall((cmd + "\r\n").encode())
        return self._readline()

    def command_multi(self, cmd):
        first = self.command(cmd)
        lines = []

        if first.startswith("+OK"):
            while True:
                line = self._readline()
                if line == ".":
                    break
                if line.startswith(".."):
                    line = line[1:]
                lines.append(line)

        return first, lines

    def login(self, user, password):
        print(self.command(f"USER {user}"))
        print(self.command(f"PASS {password}"))

    def quit(self):
        print(self.command("QUIT"))
        self.file.close()
        self.sock.close()