from socket import *

serverSock = socket(AF_INET, SOCK_STREAM) #adress_family ipv4
#socket
IP = ''
PORT = 8080
serverSock.bind((IP,PORT))#socket number and adress family connect
serverSock.listen(1)

connectionSock, addr = serverSock.accept()

msg = connectionSock.recv(1024)

print(msg.decode('utf-8'))
