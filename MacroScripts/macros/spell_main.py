import pandas as pd
import numpy as np
from main import Macro

# all_spells = pd.read_csv("./spells.csv")
all_spells = pd.read_csv("./csvData/spells2.csv")

# print(all_spells.head(10))

# firat I need to find if it is damaging, if there is a save, and attack roll

#initial parsing
# all_spells["parsed_saves"] = 0
# all_spells["damaging"] = 0
# all_spells["attack"] = 0
# for index,row in all_spells.iterrows():
#   this_save = row.saving_throw
#   if(pd.isna(this_save) != True):
#     saves = []
#     if('fort' in this_save.lower()):
#       saves.append("Fortitude")
#     if('ref' in this_save.lower()):
#       saves.append("Reflex")
#     if('will' in this_save.lower()):
#       saves.append("Will")
#     # print(this_save,saves)
#     all_spells.iloc[index,-3] = " ".join(saves)
#   if(pd.isna(row.short_description) != True):
#     if("damage" in row.short_description.lower()):
#       all_spells.iloc[index,-2] = 1
#   if(pd.isna(row.description) != True):
#     if("touch attack" in row.description.lower()):
#       all_spells.iloc[index,-1] = "touch"
#     if("ranged touch" in row.description.lower()):
#       all_spells.iloc[index,-1] = "ranged"
# all_spells.to_csv("./spells2.csv")


spell_template = '''
[h: caster_level = level]
[h: spell_level = %s]


[h: saving_throw = %s]
[h: damage_spell = %s]
[h:attack_spell = %s]

[h:roll=1d20]
[h:Touch = roll + BaB + StrMod]
[h:Ranged = roll + BaB + DexMod + SizeMod]
[h: atk_roll = %s]
[h:atk_type = "%s"]

[h:save_type = "%s"]

[h: dice = %s]
[h: ndice = %s]
[h:damage_dice=roll(ndice,dice)]
[h:damage_bonus = %s]

[h:crit_low = 20]

Casting &lt;a 
href="%s"&gt;%s&lt;/a&gt;:&lt;br&gt;
%s
[if(damage_spell == 1), code:{
	[damage_dice + damage_bonus] damage&lt;br&gt;
	};{}]
[if(attack_spell == 1),code:{
	Attack roll: [atk_roll] vs [atk_type]&lt;br&gt;
	[if(roll>=crit_low), CODE:{

Crit chance! [1d20 + BaB + StrMod] to confirm&lt;br&gt;
[damage_dice] extra damage
};{}]
[if(roll==1), CODE:{
Critical fumble!
};{}]
};{}]

[if(saving_throw == 1), code:{
	DC [10 + cstat + spell_level] [save_type]&lt;br&gt;
};{}]
'''

damaging_spells = all_spells.loc[all_spells.damaging == 1]
non_damaging_spells = all_spells.loc[all_spells.damaging == 0]
# print(damaging_spells.head())

#current order: spell level, duration, saving throw,damage?,attack?,atk type, atk type,save type, sides of dice, ndice, dmg_bon, link, name, description
def make_macro(tableRow):
  spell_level = int(tableRow.SLA_Level)
  duration = tableRow.duration
  if(pd.isna(duration)):
    duration = ""
  else:
    duration = "Duration: " + duration + "&lt;br&gt;"
  saves = tableRow.parsed_saves
  is_save = 0
  if(saves != "0"):
    is_save = 1
  damaging_spell = tableRow.damaging
  attack_spell = tableRow.attack
  atk_type = attack_spell
  if(attack_spell != "0"):
    attack_spell = 1
  
  save_type = tableRow.parsed_saves
  if(save_type == "0"):
    save_type = ""
  dice = tableRow.damage_dice
  ndice = tableRow.n_dice
  dmg_bonus = tableRow.damage_bonus
  link = tableRow.link
  name = tableRow["name"]
  desc = tableRow.short_description

  # print(name)
  file_name = name.replace(" ", "_").lower()


  command_string = (spell_template % (spell_level,is_save,damaging_spell,attack_spell,atk_type,"Touch",save_type,dice,ndice,dmg_bonus,link,name,duration))
  group_name = ("Level %s Spells" % spell_level)
  print(name)
  this_macro = Macro(label=name, command=command_string, tooltip=desc, group=group_name)
  this_macro.make_file("../../Macros/Spells/" + file_name + ".mtmacro")

 
# test = damaging_spells.iloc[10]
# make_macro(test)
    
for index,row in damaging_spells.iterrows():
  # file_path = "../../Macros/Spells/"
  make_macro(row)
for index,row in non_damaging_spells.iterrows():
  make_macro(row)