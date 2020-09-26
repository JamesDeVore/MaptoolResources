from __future__ import unicode_literals

import base64
import hashlib
import io
import os
import uuid
import pandas as pd
import numpy as np
import json
import zipfile

import jinja2
from PIL import Image
from six import iteritems


all_spells = pd.read_csv("./csvData/full_spells.csv")
all_spells.fillna('', inplace=True)


properties_xml = '''<map>
  <entry>
    <string>version</string>
    <string>1.6.1</string>
  </entry>
</map>'''

# need to insert all the spells as a list here
all_spells_list_template = '''<net.rptools.maptool.model.LookupTable_-LookupEntry>
      <min>0</min>
      <max>0</max>
      <value>%s</value>
      <imageId>
        <id>721ef64466f83a5f71d9f262176b8866</id>
      </imageId>
    </net.rptools.maptool.model.LookupTable_-LookupEntry>'''
#       <value>{&quot;spellName&quot;:&quot;Acid Arrow&quot;,&quot;school&quot;:&quot;Conjuration&quot;,&quot;subschool&quot;:&quot;Creation&quot;,&quot;descriptor&quot;:&quot;acid&quot;,&quot;spellLevel&quot;:&quot;Sorcerer/Wizard 2&quot;,&quot;spellComponents&quot;:&quot;V, S, M, F&quot;,&quot;castTime&quot;:&quot;1 standard action&quot;,&quot;range&quot;:&quot;long (400 ft. + 40 ft./level)&quot;,&quot;target&quot;:&quot;&quot;,&quot;area&quot;:&quot;&quot;,&quot;effect&quot;:&quot;one arrow of acid&quot;,&quot;duration&quot;:&quot;1 round + 1 round per three levels&quot;,&quot;savingThrow&quot;:&quot;none&quot;,&quot;spellResistance&quot;:&quot;no&quot;,&quot;shortDescription&quot;:&quot;Ranged touch attack; 2d4 damage for 1 round +1 round/three levels.&quot;,&quot;materialComponents&quot;:&quot;rhubarb leaf and an adder&apos;s stomach&quot;,&quot;focus&quot;:&quot;a dart&quot;,&quot;description&quot;:&quot;&lt;p&gt;An arrow of acid springs from your hand and speeds to its target. You must succeed on a ranged touch attack to hit your target. The arrow deals 2d4 points of acid damage with no splash damage. For every three caster levels you possess, the acid, unless neutralized, lasts for another round (to a maximum of 6 additional rounds at 18th level), dealing another 2d4 points of damage in each round.&lt;/p&gt;&quot;,&quot;reference&quot;:&quot;PFRPG Core&quot;}</value>

spell_entry_dict = {
  "spellName":"",
  "school":"",
  "subschool":"",
  "descriptor":"",
  "spellLevel":"",
  "spellComponents":"",
  "castTime":"",
  "range":"",
  "target":"",
  "area":"",
  "effect":"",
  "duration":"",
  "savingThrow":"",
  "spellResistance":"",
  "shortDescription":"",
  "materialComponents":"",
  "focus":"",
  "description":"",
  "reference":"", 
  }
spell_entry_template = '''<net.rptools.maptool.model.LookupTable_-LookupEntry>
      <min>{{ t.num }}</min>
      <max>{{t.num }}</max>
      <value>
        {{ t.allValues }}
      </value>      
    </net.rptools.maptool.model.LookupTable_-LookupEntry>'''

with open('templates/content.xml') as f:
    content_template = jinja2.Template(f.read())

entry_template = jinja2.Template(spell_entry_template)



class Entry:
  def __init__(self, **kwargs):
    for k, v in iteritems(spell_entry_dict):
        setattr(self, k, v)
    for k, v in iteritems(kwargs):
        setattr(self, k, v);
  def content_xml(self):
    if isinstance(self.allValues, str):
      self.allValues = self.allValues.replace('"',"&quot;")
    return entry_template.render(t=self)
  
all_entry_list = []
#lets make the first one a list of all spells
list_all = all_spells["spellName"].tolist()
list_entry = Entry(num = 0, allValues=list_all)
all_entry_list.append(list_entry.content_xml())

#now loop through each one and make an entry and append it
for index,temp_row in all_spells.iterrows():
  temp_entry = Entry(num = index + 1, allValues = json.dumps(temp_row.to_dict()))
  temp_xml = temp_entry.content_xml()
  all_entry_list.append(temp_xml)
final_output = content_template.render(l="".join(all_entry_list).replace("'","&quot;"))

def make_file(file, mode='w', compressed=True):
        c = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
        with zipfile.ZipFile(file, mode=mode, compression=c) as f:
            f.writestr('content.xml', final_output)
            f.writestr('properties.xml', properties_xml)
file = open("./output/content.xml","w")
file.write(final_output)
file.close()
make_file("./output/zipped/definitions.mttable")








#   # def make_file(self, file, mode='w', compressed=True):
#   #       c = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
#   #       with zipfile.ZipFile(file, mode=mode, compression=c) as f:
#   #           f.writestr('content.xml', self.content_xml())
#   #           f.writestr('properties.xml', properties_xml)

