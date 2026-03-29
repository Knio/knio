from whirl import url

def test_urls():
  assert str(url())                        == "/", url()
  assert str(url('/moo'))                  == "/moo"
  assert str(url('http://moo'))            == "http://moo/"
  assert str(url('http:///moo'))           == "http:///moo"
  assert str(url('http://moo.com'))        == "http://moo.com/"
  assert str(url('http://moo.com/'))       == "http://moo.com/"
  assert str(url('http://moo.com/foo'))    == "http://moo.com/foo"
  assert str(url('http://moo.com/foo/bar/'))                           == "http://moo.com/foo/bar/"
  assert str(url('http://moo.com/foo/bar?'))                           == "http://moo.com/foo/bar"
  assert str(url('http://moo.com/foo/bar/?var=1'))                     == "http://moo.com/foo/bar/?var=1"
  assert str(url('http://moo.com/foo/bar/?var=1&baz=dog'))             == "http://moo.com/foo/bar/?baz=dog&var=1"
  assert str(url('http://moo.com/foo/bar/?var=1&baz=dog&var=3'))       == "http://moo.com/foo/bar/?baz=dog&var=1&var=3"
  assert str(url('http://moo.com/foo/bar/?var=1&baz=dog&var=3#here'))  == "http://moo.com/foo/bar/?baz=dog&var=1&var=3#here"
  assert url('?moo=1')['moo']         == '1'
  assert str(url(url('?moo=1')))           == "/?moo=1"
  assert str(url(url('?moo=1')).update_args(bar=2))  == "/?bar=2&moo=1"
