
import pynput

def main():
  path = '/dev/input/by-id/usb-Pepper_Jobs_Limited_W11_GYRO-event-kbd'
  while 1:
    l = f.read(24)
    print(l.hex(' ', 4))

if __name__ == '__main__':
  main()
