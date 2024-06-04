'''
This code provides an implementation of a Serial class for reading and writing data from a serial port or socket. It includes subclasses SocketSerial and PySerial that provide specific implementations for reading and writing from a socket and a serial port respectively.

The Serial class has the following public APIs:
- __init__(self, timeout=2.0): Initializes the Serial object with an optional timeout value. Sets the timeout for all read operations.
- read(self, timeout=None): Read the next available bytes. Takes an optional timeout value specific to this read operation. If no bytes are available and no timeout is provided, it uses the default timeout value set in the constructor.
- write(self, data): Write data to the serial port or socket.
- read_until(self, footer, timeout=None): Read data until the specified footer is found. Takes an optional timeout value specific to this read operation. If the footer is not found and no timeout is provided, it uses the default timeout value set in the constructor.
- read_all(self, timeout=None): Read all available bytes until the read times out. Takes an optional timeout value specific to this read operation. If no timeout is provided, it uses the default timeout value set in the constructor.

The Serial class also has internal methods:
- set_timeout(self, t): Sets the timeout value for the serial port or socket.
- read_raw(self, n): Implementation of reading raw bytes from the serial port or socket. Subclasses should override this method.
- write_raw(self, data): Implementation of writing raw bytes to the serial port or socket. Subclasses should override this method.

The Serial class has an internal variable:
- rq: A list to store any leftover data from incomplete read operations.
- timeout: The timeout value for all read operations.

The SocketSerial class is a subclass of Serial and provides an implementation for reading and writing from a socket. It has an additional public API:
- __init__(self, sock, *args, **kwargs): Initializes the SocketSerial object and takes a socket object as a required argument. Any additional arguments and keyword arguments are passed to the parent class constructor.

The SocketSerial class overrides the following internal methods from the Serial class:
- set_timeout(self, t): Sets the timeout value for the socket.
- read_raw(self, n): Implementation of reading raw bytes from the socket.
- write_raw(self, data): Implementation of writing raw bytes to the socket.

The PySerial class is a subclass of Serial and provides an implementation for reading and writing from a serial port using the PySerial library. It has an additional public API:
- __init__(self, ser, *args, **kwargs): Initializes the PySerial object and takes a PySerial serial port object as a required argument. Any additional arguments and keyword arguments are passed to the parent class constructor.

The PySerial class overrides the following internal methods from the Serial class:
- set_timeout(self, t): Sets the timeout value for the serial port.
- read_raw(self, n): Implementation of reading raw bytes from the serial port.
- write_raw(self, data): Implementation of writing raw bytes to the serial port.
- read_until(self, footer, timeout=None): Implementation of reading until the specified footer is found from the serial port.

The PySerial class also has an internal variable:
- ser: The PySerial serial port object.
'''

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
    # LOG.debug(f'write: {data!r}')
    while data:
      n = self.write_raw(data)
      data = data[n:]

  def read_until(self, footer, timeout=None):
    if timeout is None:
      timeout = self.timeout
    # end = time.time() + timeout
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

  def set_timeout(self, t):
    raise NotImplementedError
  def read_raw(self, n):
    raise NotImplementedError
  def write_raw(self, data):
    raise NotImplementedError


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
    if self.ser.timeout != t:
      LOG.warning(
        'WARNING! setting timeout on pyserial.Serial '
        'while a connection is active will corrupt the read buffer')
      self.ser.timeout = t
      self.ser.reset_input_buffer()

  def read_raw(self, n):
    # compensate for weird pyserial behavior
    # wait for at least 1 byte
    buf = self.ser.read(1)
    if not buf:
      return buf
    # flush any remaining bytes
    k = min(n - 1, self.ser.in_waiting)
    if k:
      buf += self.ser.read(k)
    return buf

  def write_raw(self, data):
    return self.ser.write(data)

  def read_until(self, footer, timeout=None):
    if timeout is None:
      timeout = self.timeout
    self.set_timeout(timeout)
    b = b''.join(self.rq)
    self.rq[:] = []
    i = b.find(footer)
    if i == -1:
      b += self.ser.read_until(footer)
    i = b.find(footer)
    if i == -1:
      self.rq.append(b)
      return b''
    i += len(footer)
    b, q = b[:i], b[i:]
    self.rq.append(q)
    return b
