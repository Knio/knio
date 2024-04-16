import socket

def main():
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  # sock.bind(('255.255.255.255', 8367))
  sock.bind(('', 8367))
  sock.settimeout(1)
  while 1:
    try:
      data = sock.recvfrom(1024)
      print(data)
    except socket.timeout:
      print('.', end='', flush=True)

if __name__ == '__main__':
  main()
