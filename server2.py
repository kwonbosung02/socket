import socketserver
import threading

HOST = ''
PORT = 9009
lock = threading.Lock()

class UserManager:
    def __init__(self):
        self.users = {}

    def addUser(self, username, conn, addr):
        if username in self.users:
            print("이미 등록된 이름입니다.".encode())
            return None
        lock.acquire()
        self.users[username] = (conn,addr)
        lock.release()
        self.messageToAll('[%s] joined' %username)
        print("---Members [%d]---" %len(self.users))
        return username

    def removeUser(self,username):
        if username not in self.users:
            return
        lock.acquire()
        del self.users[username]
        lock.release()

        self.messageToAll('[%s] exit' %username)
        print("---Members [%d]---" %len(self.users))

    def messageHandle(self, username, msg):
        if msg[0] != '/':
            self.messageToAll('[%s] %s'%(username, msg))
            return
        if msg.strip() =='/quit':
            self.removeUser(username)
            return -1
    def messageToAll(self,msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())

class tcpHandler(socketserver.BaseRequestHandler):
    userm = UserManager()

    def handle(self):
        print("[%s] connected"%self.client_address[0])

        try:
            username = self.registerUserName()
            msg = self.request.recv(1024)
            while msg:
                print('['+username+']' +msg.decode())
                if(self.userm.messageHandle(username, msg.decode()) == -1):
                    self.request.close()
                    break
                msg = self.request.recv(1024)
        except Exception as e:
            print(e)
    def registerUserName(self):
        while True:
            self.request.send('login ID:'.encode())
            username =self.request.recv(1024)
            username = username.decode().strip()
            if self.userm.addUser(username, self.request, self.client_address):
                return username

class ChatServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

def runServer():
    print('running...')
    print('exit chat ctrl-c')
    try:
        server = ChatServer((HOST,PORT), tcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('exit...')
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    runServer()
