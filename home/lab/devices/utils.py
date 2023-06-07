import time

class Serial:
  def __init__(self, timeout=2.0):
    self.rq = []
    self.timeout = timeout
    self.set_timeout(timeout)

  def read(self):
    if self.rq:
      return self.rq.pop(0)
    return self.read_raw(1024)

  def read_until(self, footer):
    end = time.time() + self.timeout
    buf = b''
    while 1:
      remaining = end - time.time()
      if remaining < 0:
        raise TimeoutError(buf)
      self.set_timeout(remaining)
      d = self.read()
      buf += d
      if (n := buf.find(footer)) != -1:
        break

    n += len(footer)
    self.set_timeout(self.timeout)
    self.rq.append(buf[n:])
    return buf[:n]


class PySerial(Serial):
  def __init__(self, ser, *args, **kwargs):
    self.ser = ser
    super().__init__(*args, **kwargs)

  def set_timeout(self, t):
    self.ser.timeout = t

  def read_raw(self, n):
    # compensate for weird pyserial behavior
    # t = self.ser.timeout
    # wait for at least 1 byte
    buf = self.ser.read(1)
    if not buf:
      return buf
    # flush any remaining bytes
    # self.ser.timeout = 0
    k = min(n - 1, self.ser.in_waiting)
    if k:
      buf += self.ser.read(k)
    # self.ser.timeout = t
    return buf
