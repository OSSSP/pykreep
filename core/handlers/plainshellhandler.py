import socket as s

class PlainShellHandler:
    def __init__(self, sock: s.socket):
        if not sock:
            raise ValueError('sock is None')
        self.sock = sock

    def handle_shell(self):
        self.sock.settimeout(0.1)

        while True:
            try:
                data = b''

                while True:
                    try:
                        data += self.sock.recv(4096)
                    except s.timeout:
                        break

                print(data.decode('ascii'))

                data = input('Shell>')
                if data == 'exit':
                    print('quitting shell')
                    self.sock.close()
                    return

                self.sock.send((data + '\n').encode('ascii'))
            except KeyboardInterrupt:
                print('Exiting shell')
                self.sock.close()
                return

