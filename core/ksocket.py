import socket
import core.errors


class KSocket:
    def __init__(self, sock: socket.socket):
        if not sock:
            raise ValueError('sock is null')
        self.sock = sock

    def readex(self, nbytes: int) -> bytes:
        chunks = b''
        bytes_recd = 0
        while bytes_recd < nbytes:
            chunk = self.sock.recv(min(nbytes - bytes_recd, 2048))
            if not chunk:
                raise core.errors.ConnectionTerminatedError('Connection terminated in readex()')
            chunks += chunk
            bytes_recd = bytes_recd + len(chunk)
        return chunks

    def sendex(self, msg: bytes) -> None:
        total_sent = 0
        while total_sent < len(msg):
            sent = self.sock.send(msg[total_sent:])
            if sent == 0:
                raise core.errors.ConnectionTerminatedError('Connection terminated in sendex()')
            total_sent += sent


