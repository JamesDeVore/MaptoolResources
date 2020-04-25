from __future__ import unicode_literals

import base64
import hashlib
import io
import os
import uuid
import zipfile

import jinja2
from PIL import Image
from six import iteritems


properties_xml = '''<map>
  <entry>
    <string>version</string>
    <string>1.6.1</string>
  </entry>
</map>'''

with open('templates/content.xml') as f:
    content_template = jinja2.Template(f.read())
    
macro_defaults = {
    'command': '',
    'label': '',
    'group': '',
    'sortby': '',
    'color': 'default',
    'font_color': 'black',
    'font_size': '1.00em',
    'tooltip': '',
    'hotkey': 'None',
}



class Macro:
  def __init__(self, **kwargs):
    for k, v in iteritems(macro_defaults):
        setattr(self, k, v)
    for k, v in iteritems(kwargs):
        setattr(self, k, v);
  def content_xml(self):
    return content_template.render(m=self)

  def make_file(self, file, mode='w', compressed=True):
        c = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
        with zipfile.ZipFile(file, mode=mode, compression=c) as f:
            f.writestr('content.xml', self.content_xml())
            f.writestr('properties.xml', properties_xml)

