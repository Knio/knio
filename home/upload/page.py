import pathlib
import dominate
from dominate import tags, util
from dominate.tags import *

ASSETS = pathlib.Path(__file__).parent

class uploadui(dominate.document):
  def __init__(self):
    super().__init__(title='Upload')

    with self.head:
      meta(charset='utf-8')
      meta(name='viewport', content='width=device-width, initial-scale=1.0')
      # style(util.include(ASSETS / 'reset.css'))
      style(util.include(ASSETS / 'upload.css'))

    with self.body:
      with div(id='upload'):
        with form(action='/updo', method='post', enctype='multipart/form-data'):
          input_(type='checkbox', id='toirc', name='toirc', checked=True)
          label('Post to IRC?', fr='toirc')
          p('Share something')

          SEP = i('～ or ～')
          p('————————————')
          input_(type='file', name='file', multiple=True)
          # input_(type='submit', value='Upload')

          p(SEP)
          p(i('Paste (ctrl-v) or Drag file here'))

          p(SEP)
          p("\n$ curl https://img.zkpq.ca/updo -X POST -F 'file=@your_file.jpg' ")

          p(SEP)
          p("\n$ wget https://img.zkpq.ca/updo --method=POST --body-file 'your_file.jpg' ")


        div(id='preview')
        div(id='log')


      script(util.include(ASSETS / 'upload.js'))
