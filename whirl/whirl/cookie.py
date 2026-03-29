import datetime

class cookie:
  def __init__(self, name, value, expires=None, duration=None, path='/',
               domain=None, secure=False, httponly=False):

    if duration and expires:
        raise ValueError('Cookie cannot have both expiry date and duration.')

    self.name     = name.lower()
    self.value    = value
    self.path     = path
    self.expires  = expires
    self.duration = duration
    self.domain   = domain
    self.secure   = secure
    self.httponly = httponly

  def render(self, is_header=False):
    timestamp = None
    if self.expires:
      if isinstance(self.expires, datetime.datetime):
        timestamp = self.expires
      elif isinstance(self.expires, float) or \
           isinstance(self.expires, int):
        timestamp = datetime.datetime.utcfromtimestamp(self.expires)
      else:
        raise TypeError('Invalid expiry time.')
    if self.duration:
      timestamp = datetime.datetime.utcnow()
      if isinstance(self.duration, float) or \
          isinstance(self.duration, int):
         timestamp += datetime.timedelta(seconds=self.duration)
      else:
        raise TypeError('Invalid duration.')

    cookie = []
    cookie.append('%s=%s;' % (self.name, self.value))
    cookie.append('path=%s;' % self.path)
    if timestamp:     cookie.append('expires=%s;' % timestamp.strftime("%a, %d-%b-%Y %H:%M:%S GMT"))
    if self.domain:   cookie.append('domain=%s;' % self.domain)
    if self.secure:   cookie.append('secure;')
    if self.httponly: cookie.append('httponly;')

    return ('Set-Cookie: ' if is_header else '') + ' '.join(cookie)

  def __str__(self):
    return self.render()
  __unicode__ = __str__

  def __repr__(self):
    return "<whirl.cookie %s>" % self.render()
