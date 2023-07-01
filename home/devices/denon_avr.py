'''
'''

import socket
import logging

import utils

class DenonAVR:
  def __init__(self, host):
    self.host = host
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(1)
    self.socket.connect((self.host, 21))
    self.ser = SocketSerial(self.socket)


  def query(self, query):
    self.ser.write(query + b'\r')
    return self.ser.



  def get_power(self):
    r = self.query(b'PW?')



def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM9')
  args = parser.parse_args()

  ser = serial.Serial(
    args.port,
    baudrate=115200,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=1.
  )


  xdm = XDM1041(ser)
  xdm.foo()


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
