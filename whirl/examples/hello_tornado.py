import logging

import whirl.tornado_server as ts

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)

  # Example usage
  @ts.get('^/$')
  def index(request):
    return 'Hello World'

  @ts.get('^/u/([a-z0-9]+)$')
  def user(request, name):
    return 'Hi, %s' % name

  ts.run()
