import time
import rebugger


def fail():
  return 1/0

def add(a, b):
  return a + b

def hello():
  time.sleep(0.001)
  try:
    num = fail()
  except:
    num = add(1, 2)

  print(f'Hello world! {num}')

if __name__ == '__main__':
  rebugger.start()
  hello()
  # rebugger.finish() # oops i forgot to call finish
