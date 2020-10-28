import socket
import json
import sys
import re

LOCALHOST = "127.0.0.1"
PORT = 9001
SEPARATOR = ";"
MAX_SIZE = 40000

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    @staticmethod
    def encode_decode(text, key):
        return "".join([chr(ord(a) ^ ord(b)) for a, b in zip(text, key)])
    
    @staticmethod
    def swap(text, jsonf):
        jsonf = json.loads(jsonf)
        for key in jsonf.keys():
            text = re.sub(key, jsonf[key], text, flags=re.IGNORECASE)
        return text

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()

        print(f"Server started on {sock.getsockname()}")

        while True:
            try:
                conn, addr = sock.accept()
                print(f"Connection from {addr}")

                received = conn.recv(32).decode("ascii")
                mode, text_size, jk_size = received.split(SEPARATOR)
                text_size = int(text_size)
                jk_size = int(jk_size)
                if text_size > MAX_SIZE or jk_size > MAX_SIZE:
                    print(f"Client {addr} sent too big files. Closing connection.")
                    conn.close()
                    continue

                print(f"Receiving text file from {addr}...")
                text = conn.recv(text_size).decode("ascii")

                print(f"Receiving {'json' if mode == 'change_text' else 'key'} file from {addr}...")
                jk = conn.recv(jk_size).decode("ascii")

                if mode == "change_text":
                    swapped = self.swap(text, jk)
                    print(f"Sending swapped file to {addr}...")
                    conn.sendall(swapped.encode("ascii"))
                else:
                    encoded = self.encode_decode(text, jk)
                    print(f"Sending encoded file to {addr}...")
                    conn.sendall(encoded.encode("ascii"))
                    
                    decoded = self.encode_decode(encoded, jk)
                    print(f"Sending decoded file to {addr}...")
                    conn.sendall(decoded.encode("ascii"))
                conn.close()
                
            except KeyboardInterrupt:
                print('Server is being closed.')
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                break
            except:
                conn.close()
                print("There was an error.")
                continue
            finally:
                print()
            

def main():
    Server(LOCALHOST, PORT).start()

if __name__ == "__main__":
    main()