import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))
message ="Player"
s.send(message.encode())


while 1:
  data = s.recv(1024).decode()
  print("received:",data)
  s.send(input().encode())
  