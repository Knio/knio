
import logging
import time

LOG = logging.getLogger(__name__)



class Serial:
  def __init__(self, timeout=2.0):
    # TODO add encoding param
    self.rq = []
    self.timeout = timeout
    self.set_timeout(timeout)

  def read(self, timeout=None):
    '''
    return the next available bytes
    '''
    if self.rq:
      return self.rq.pop(0)
    if timeout is None:
      timeout = self.timeout
    self.set_timeout(timeout)
    return self.read_raw(1024)

  def write(self, data):
    LOG.debug(f'write: {data!r}')
    while data:
      n = self.write_raw(data)
      data = data[n:]

  def read_until(self, footer, timeout=None):
    if timeout is None:
      timeout = self.timeout
    end = time.time() + timeout
    buf = b''
    n = -1
    done = False
    while not done:
      d = self.read(0)
      if not d:
        d = self.read(timeout)
        done = True
      buf += d
      if (n := buf.find(footer)) != -1:
        break

    if n == -1:
      self.rq.append(buf)
      return b''

    n += len(footer)
    self.rq.append(buf[n:])
    r = buf[:n]
    LOG.debug(f'read_until: {r!r}')
    return r

  def read_all(self, timeout=None):
    if timeout is None:
      timeout = self.timeout
    self.set_timeout(timeout)
    r = []
    while b := self.read(timeout):
      r.append(b)
    r = b''.join(r)
    LOG.debug(f'flush: {r!r}')
    return r


class SocketSerial(Serial):
  def __init__(self, sock, *args, **kwargs):
    self.sock = sock
    super().__init__(*args, **kwargs)

  def set_timeout(self, t):
    self.sock.settimeout(t)

  def read_raw(self, n):
    try:
      return self.sock.recv(n)
    except (BlockingIOError, TimeoutError):
      return b''

  def write_raw(self, data):
    return self.sock.send(data)


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
