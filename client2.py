import socket
from threading import Thread

HOST = 'localhost'
PORT = 9009

def rcvMsg(sock):
    while True:
        try:
            da = sock.recv(1024)
            if not da:
                break
            print(da.decode())
        except:
            pass

def runChat():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        t = Thread(target=rcvMsg, args=(sock,))
        t.daemon = True
        t.start()

        while True:
            msg = input()
            if msg == '/quit':
               sock.send(msg.encode())
               break
            sock.send(msg.encode())

if __name__ == "__main__":
    runChat()
