from __future__ import unicode_literals

import base64
import hashlib
import io
import os
import uuid
import pandas as pd
import numpy as np
import json

import jinja2
from PIL import Image
from six import iteritems


all_spells = pd.read_csv("./csvData/spell_index.csv")


properties_xml = '''<map>
  <entry>
    <string>version</string>
    <string>1.6.1</string>
  </entry>
</map>'''

#       <value>[{&apos;dndClass&apos;:&apos;Bard&apos;},{&apos;dndClass&apos;:&apos;Cleric&apos;},{&apos;dndClass&apos;:&apos;Druid&apos;},{&apos;dndClass&apos;:&apos;Paladin&apos;},{&apos;dndClass&apos;:&apos;Ranger&apos;},{&apos;dndClass&apos;:&apos;Sorcerer/Wizard&apos;},{&apos;domain&apos;:&apos;Air&apos;},{&apos;domain&apos;:&apos;Animal&apos;},{&apos;domain&apos;:&apos;Artifice&apos;},{&apos;domain&apos;:&apos;Chaos&apos;},{&apos;domain&apos;:&apos;Charm&apos;},{&apos;domain&apos;:&apos;Community&apos;},{&apos;domain&apos;:&apos;Darkness&apos;},{&apos;domain&apos;:&apos;Death&apos;},{&apos;domain&apos;:&apos;Destruction&apos;},{&apos;domain&apos;:&apos;Earth&apos;},{&apos;domain&apos;:&apos;Evil&apos;},{&apos;domain&apos;:&apos;Fire&apos;},{&apos;domain&apos;:&apos;Glory&apos;},{&apos;domain&apos;:&apos;Good&apos;},{&apos;domain&apos;:&apos;Healing&apos;},{&apos;domain&apos;:&apos;Knowledge&apos;},{&apos;domain&apos;:&apos;Law&apos;},{&apos;domain&apos;:&apos;Liberation&apos;},{&apos;domain&apos;:&apos;Luck&apos;},{&apos;domain&apos;:&apos;Madness&apos;},{&apos;domain&apos;:&apos;Magic&apos;},{&apos;domain&apos;:&apos;Nobility&apos;},{&apos;domain&apos;:&apos;Plant&apos;},{&apos;domain&apos;:&apos;Protection&apos;},{&apos;domain&apos;:&apos;Repose&apos;},{&apos;domain&apos;:&apos;Rune&apos;},{&apos;domain&apos;:&apos;Strength&apos;},{&apos;domain&apos;:&apos;Sun&apos;},{&apos;domain&apos;:&apos;Travel&apos;},{&apos;domain&apos;:&apos;Trickery&apos;},{&apos;domain&apos;:&apos;War&apos;},{&apos;domain&apos;:&apos;Water&apos;},{&apos;domain&apos;:&apos;Weather&apos;},{&apos;school&apos;:&apos;Abjuration&apos;},{&apos;school&apos;:&apos;Conjuration&apos;},{&apos;school&apos;:&apos;Divination&apos;},{&apos;school&apos;:&apos;Enchantment&apos;},{&apos;school&apos;:&apos;Evocation&apos;},{&apos;school&apos;:&apos;Illusion&apos;},{&apos;school&apos;:&apos;Necromancy&apos;},{&apos;school&apos;:&apos;Transmutation&apos;},{&apos;school&apos;:&apos;Universal&apos;},{&apos;alpha&apos;:&apos;A&apos;},{&apos;alpha&apos;:&apos;B&apos;},{&apos;alpha&apos;:&apos;C&apos;},{&apos;alpha&apos;:&apos;D&apos;},{&apos;alpha&apos;:&apos;E&apos;},{&apos;alpha&apos;:&apos;F&apos;},{&apos;alpha&apos;:&apos;G&apos;},{&apos;alpha&apos;:&apos;H&apos;},{&apos;alpha&apos;:&apos;I&apos;},{&apos;alpha&apos;:&apos;J&apos;},{&apos;alpha&apos;:&apos;K&apos;},{&apos;alpha&apos;:&apos;L&apos;},{&apos;alpha&apos;:&apos;M&apos;},{&apos;alpha&apos;:&apos;N&apos;},{&apos;alpha&apos;:&apos;O&apos;},{&apos;alpha&apos;:&apos;P&apos;},{&apos;alpha&apos;:&apos;Q&apos;},{&apos;alpha&apos;:&apos;R&apos;},{&apos;alpha&apos;:&apos;S&apos;},{&apos;alpha&apos;:&apos;T&apos;},{&apos;alpha&apos;:&apos;U&apos;},{&apos;alpha&apos;:&apos;V&apos;},{&apos;alpha&apos;:&apos;W&apos;},{&apos;alpha&apos;:&apos;X&apos;},{&apos;alpha&apos;:&apos;Y&apos;},{&apos;alpha&apos;:&apos;Z&apos;},{&apos;subschool&apos;:&apos;Calling&apos;},{&apos;subschool&apos;:&apos;Compulsion&apos;},{&apos;subschool&apos;:&apos;Creation&apos;},{&apos;subschool&apos;:&apos;Figment&apos;},{&apos;subschool&apos;:&apos;Glamer&apos;},{&apos;subschool&apos;:&apos;Healing&apos;},{&apos;subschool&apos;:&apos;Pattern&apos;},{&apos;subschool&apos;:&apos;Phantasm&apos;},{&apos;subschool&apos;:&apos;Polymorph&apos;},{&apos;subschool&apos;:&apos;Scrying&apos;},{&apos;subschool&apos;:&apos;Shadow&apos;},{&apos;subschool&apos;:&apos;Summoning&apos;},{&apos;subschool&apos;:&apos;Teleportation&apos;},{&apos;descriptor&apos;:&apos;acid&apos;},{&apos;descriptor&apos;:&apos;air&apos;},{&apos;descriptor&apos;:&apos;chaotic&apos;},{&apos;descriptor&apos;:&apos;cold&apos;},{&apos;descriptor&apos;:&apos;creation&apos;},{&apos;descriptor&apos;:&apos;darkness&apos;},{&apos;descriptor&apos;:&apos;death&apos;},{&apos;descriptor&apos;:&apos;earth&apos;},{&apos;descriptor&apos;:&apos;electricity&apos;},{&apos;descriptor&apos;:&apos;evil&apos;},{&apos;descriptor&apos;:&apos;fear&apos;},{&apos;descriptor&apos;:&apos;fire&apos;},{&apos;descriptor&apos;:&apos;force&apos;},{&apos;descriptor&apos;:&apos;good&apos;},{&apos;descriptor&apos;:&apos;language-dependent&apos;},{&apos;descriptor&apos;:&apos;lawful&apos;},{&apos;descriptor&apos;:&apos;light&apos;},{&apos;descriptor&apos;:&apos;mind-affecting&apos;},{&apos;descriptor&apos;:&apos;sonic&apos;},{&apos;descriptor&apos;:&apos;water&apos;}]</value>

#

index_types = [
{'dndClass':'Bard'},
{'dndClass':'Cleric'},
{'dndClass':'Druid'},
{'dndClass':'Paladin'},
{'dndClass':'Ranger'},
{'dndClass':'Sorcerer'},
{'dndClass':'Wizard'},
{'dndClass':'Alchemist'},
{'dndClass':'Summoner'},
{'dndClass':'Inquisitor'},
{'dndClass':'Oracle'},
{'dndClass':'Antipaladin'},
{'dndClass':'Magus'},
{'dndClass':'Adept'},
{'dndClass':'Bloodrager'},
{'dndClass':'Shaman'},
{'dndClass':'Psychic'},
{'dndClass':'Medium'},
{'dndClass':'Mesmerist'},
{'dndClass':'Occultist'},
{'dndClass':'Spiritualist'},
{'dndClass':'Skald'},
{'dndClass':'Investigator'},
{'dndClass':'Hunter'},
# {'domain':'Air'},
# {'domain':'Animal'},
# {'domain':'Artifice'},
# {'domain':'Chaos'},
# {'domain':'Charm'},
# {'domain':'Community'},
# {'domain':'Darkness'},
# {'domain':'Death'},
# {'domain':'Destruction'},
# {'domain':'Earth'},
# {'domain':'Evil'},
# {'domain':'Fire'},
# {'domain':'Glory'},
# {'domain':'Good'},
# {'domain':'Healing'},
# {'domain':'Knowledge'},
# {'domain':'Law'},
# {'domain':'Liberation'},
# {'domain':'Luck'},
# {'domain':'Madness'},
# {'domain':'Magic'},
# {'domain':'Nobility'},
# {'domain':'Plant'},
# {'domain':'Protection'},
# {'domain':'Repose'},
# {'domain':'Rune'},
# {'domain':'Strength'},
# {'domain':'Sun'},
# {'domain':'Travel'},
# {'domain':'Trickery'},
# {'domain':'War'},
# {'domain':'Water'},
# {'domain':'Weather'},
{'school':'Abjuration'},
{'school':'Conjuration'},
{'school':'Divination'},
{'school':'Enchantment'},
{'school':'Evocation'},
{'school':'Illusion'},
{'school':'Necromancy'},
{'school':'Transmutation'},
{'school':'Universal'},
{'alpha':'A'},
{'alpha':'B'},
{'alpha':'C'},
{'alpha':'D'},
{'alpha':'E'},
{'alpha':'F'},
{'alpha':'G'},
{'alpha':'H'},
{'alpha':'I'},
{'alpha':'J'},
{'alpha':'K'},
{'alpha':'L'},
{'alpha':'M'},
{'alpha':'N'},
{'alpha':'O'},
{'alpha':'P'},
{'alpha':'Q'},
{'alpha':'R'},
{'alpha':'S'},
{'alpha':'T'},
{'alpha':'U'},
{'alpha':'V'},
{'alpha':'W'},
{'alpha':'Y'},
{'alpha':'Z'}
# {'subschool':'Calling'},
# {'subschool':'Compulsion'},
# {'subschool':'Creation'},
# {'subschool':'Figment'},
# {'subschool':'Glamer'},
# {'subschool':'Healing'},
# {'subschool':'Pattern'},
# {'subschool':'Phantasm'},
# {'subschool':'Polymorph'},
# {'subschool':'Scrying'},
# {'subschool':'Shadow'},
# {'subschool':'Summoning'},
# {'subschool':'Teleportation'},
# {'descriptor':'acid'},
# {'descriptor':'air'},
# {'descriptor':'chaotic'},
# {'descriptor':'cold'},
# {'descriptor':'creation'},
# {'descriptor':'darkness'},
# {'descriptor':'death'},
# {'descriptor':'earth'},
# {'descriptor':'electricity'},
# {'descriptor':'evil'},
# {'descriptor':'fear'},
# {'descriptor':'fire'},
# {'descriptor':'force'},
# {'descriptor':'good'},
# {'descriptor':'language-dependent'},
# {'descriptor':'lawful'},
# {'descriptor':'light'},
# {'descriptor':'mind-affecting'},
# {'descriptor':'sonic'},
# {'descriptor':'water'}
]

entry_template = '''
<net.rptools.maptool.model.LookupTable_-LookupEntry>
      <min>{{ t.num }}</min>
      <max>{{t.num }}</max>
      <value>{{ t.allValues }}</value>      
    </net.rptools.maptool.model.LookupTable_-LookupEntry>
    '''

with open('templates/content.xml') as f:
    content_template = jinja2.Template(f.read())

entry_template = jinja2.Template(entry_template)



class Entry:
  def __init__(self, **kwargs):
    for k, v in iteritems(kwargs):
        setattr(self, k, v);
  def content_xml(self):
    if isinstance(self.allValues, str):
      self.allValues = self.allValues.replace('"',"&apos;")
    return entry_template.render(t=self)
  
all_entry_list = []
#lets make the first one a list of all spells
list_all = json.dumps(index_types)
list_entry = Entry(num = 0, allValues=list_all)
all_entry_list.append(list_entry.content_xml())

# print(all_entry_list)
#now loop through each one and make an entry and append it
index = 1
for test_entry in index_types:
  final_list = []
  entry_type = list(test_entry.keys())[0]
  if(entry_type == "dndClass"):
    className = test_entry["dndClass"]
    filtered = all_spells.dropna(subset=[className])
    max_lvl = int(filtered[className].max())
    # print(filtered[["name",className]])
    for lvl in range(0,max_lvl + 1):
      filteredSpells = filtered.loc[filtered[className] == lvl]
      this_lvl_spells = filteredSpells.index.tolist()
      final_list.append(this_lvl_spells)
  if(entry_type == "school"):
    domain = test_entry["school"]
    filtered = all_spells.loc[all_spells["school"] == domain]
    max_lvl = int(filtered["SLA_Level"].max())
    for lvl in range(0,max_lvl + 1):
      filteredSpells = filtered.loc[filtered["SLA_Level"] == lvl]
      this_lvl_spells = filteredSpells.index.tolist()
      final_list.append(this_lvl_spells)
  if(entry_type == "alpha"):
    letter = test_entry["alpha"][0]
    filtered = all_spells.loc[all_spells["name"].str.startswith(letter)]
    print(filtered)
    max_lvl = int(filtered["SLA_Level"].max())

    for lvl in range(0,max_lvl + 1):
      filteredSpells = filtered.loc[filtered["SLA_Level"] == lvl]
      this_lvl_spells = filteredSpells.index.tolist()
      final_list.append(this_lvl_spells)
  spell_entry = Entry(num = index, allValues = final_list)
  all_entry_list.append(spell_entry.content_xml())








  index+=1
# for index,temp_row in all_spells.iterrows():
#   temp_entry = Entry(num = index + 1, allValues = json.dumps(temp_row.to_dict()))
#   temp_xml = temp_entry.content_xml()
#   all_entry_list.append(temp_xml)
final_output = content_template.render(l="".join(all_entry_list).replace("'","&quot;"))
file = open("./output/index_content.xml","w")
file.write(final_output)
file.close()








#   # def make_file(self, file, mode='w', compressed=True):
#   #       c = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
#   #       with zipfile.ZipFile(file, mode=mode, compression=c) as f:
#   #           f.writestr('content.xml', self.content_xml())
#   #           f.writestr('properties.xml', properties_xml)

