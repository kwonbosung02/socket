from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))

print('connected')

clientSock.send('hello'.encode('utf-8'))

print('send')
