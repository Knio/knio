import datetime
import http.server
import socketserver
import logging
import json
import time

LOG = logging.getLogger('phone')

ADDR = ('localhost', 11002)
ADDR = ('', 11002)


class HttpServer(socketserver.ThreadingMixIn, http.server.BaseHTTPRequestHandler):
  @classmethod
  def run(cls, addr=ADDR):
    class SS(socketserver.TCPServer):
      def handle_timeout(self):
        super().handle_timeout()
        raise TimeoutError

    httpd = SS(addr, cls, bind_and_activate=False)
    httpd.allow_reuse_address = True
    httpd.daemon_threads = True
    httpd.timeout = 1
    httpd.server_bind()
    httpd.server_activate()

    LOG.info(f'Serving at {addr}')
    n = -60 * 60
    try:
      while n:
        n += 1
        try:
          httpd.handle_request()
        except TimeoutError:
          pass
        except KeyboardInterrupt as e:
          LOG.info(f'Stopping server: {e!r}')
          break
    finally:
      httpd.server_close()
    LOG.info('done')

  def do_GET(self):
    return self.do('get')

  def do_POST(self):
    return self.do('post')

  def do(self, method):
    data = None
    try:
      cl = int(self.headers.get('Content-Length', 0))
      data = self.rfile.read(cl).decode('utf8', errors='replace')
      data = json.loads(data)
    except:
      LOG.exception('oopsie')

    dt = datetime.datetime.now().astimezone()
    log = dict(
      type='http',
      time=time.time(),
      datetime=dt.isoformat(),
      headers=dict(self.headers),
      address=self.address_string(),
      request=self.requestline,
      path=self.path,
      command=self.command,
      data=data,
    )

    js = json.dumps(log, sort_keys=True, indent=2)
    print(js)
    LOG.info(js)

    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.end_headers()
    self.wfile.write(b'ok')
    self.close_connection = True



def main():
  HttpServer.run()


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    datefmt='%y%m%d-%H%M%S',
    level=logging.INFO,
  )
  main()
