import socket

addr = '83:E5:F9:5B:A9:0F'
port = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((addr, port))

while 1:
    d = s.recv(1024)
    print(f'>> {d} ;')

