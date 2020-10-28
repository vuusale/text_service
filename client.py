import argparse
import socket
import os
import magic
import sys

LOCALHOST = "127.0.0.1"
PORT = 9001
SEPARATOR = ";"

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self, mode, text_file, jk_file):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((LOCALHOST, PORT))
            text_size = os.path.getsize(text_file)
            jk_size = os.path.getsize(jk_file)
            msg = f"{mode}{SEPARATOR}{text_size}{SEPARATOR}{jk_size}"
            sock.send(msg.encode("ascii"))

            f = open(text_file, "r")
            fcontent = f.read()
            f.close()
            print("Sending text file...")
            sock.sendall(fcontent.encode("ascii"))
            
            f = open(jk_file, "r")
            jkcontent = f.read()
            f.close()
            print(f"Sending {'json' if mode == 'change_text' else 'key'} file...")
            sock.sendall(jkcontent.encode("ascii"))

            result = sock.recv(text_size).decode("ascii")
            print(f"Answer from the server:\n\n{result}\n")

            if mode == "encode_decode":
                decoded = sock.recv(text_size).decode("ascii")
                print(f"Encoding accuracy verified ✓" if decoded == fcontent else "There is a mistake in encoding ❌")
            sock.close()
            
        except socket.timeout:
            print("Connection couldn't be created.")
        except ConnectionRefusedError:
            print("Server cannot be reached.")
        except BrokenPipeError:
            print("Connection closed. Probably files are too big.")
        except ConnectionResetError:
            print("Connection closed due to an error.")
        except:
            print("There was an error.")


def main():
    choices = {"change_text", "encode_decode"}
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m", metavar="MODE", type=str, help="Service type", choices=choices)
    parser.add_argument("--text_file", "-t", metavar="TEXT_FILE", type=str, help="Text file")
    parser.add_argument("--jk_file", "-k", metavar="JK_FILE", type=str, help="JSON or key file")
    args = parser.parse_args()
    if magic.from_file(args.text_file, mime=True) != "text/plain" or \
        (args.mode == "change_text" and magic.from_file(args.jk_file, mime=True) != "application/json") or \
        (args.mode == "encode_decode" and magic.from_file(args.jk_file, mime=True) != "text/plain"):
        print(f"Filetype error.")
        sys.exit(1)
    Client(LOCALHOST, PORT).connect(args.mode, args.text_file, args.jk_file)

if __name__ == "__main__":
    main()