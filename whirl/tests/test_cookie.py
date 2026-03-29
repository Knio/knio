
import whirl

def test_cookie():
  assert whirl.cookie('foo', 'bar').render() == 'foo=bar; path=/;'



