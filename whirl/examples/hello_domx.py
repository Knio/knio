import logging

import whirl.domx_server as dx
from dominate.tags import *

class Hello(dx.Page):
  @div
  def index(self):
    h1('Hello world')
    button('foo', dx.x(target='#content', get='/foo'))
    button('bar', dx.x(target='#content', get='/bar'))
    with div(id='content'):
      self.foo()

  @div
  def foo(self):
    h3('asdf asdf')

  @div
  def bar(self):
    h3('lorem ipsum')



if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  dx.run(Hello)
