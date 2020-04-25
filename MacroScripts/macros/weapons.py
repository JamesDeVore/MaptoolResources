import pandas as pd
from main import Macro

all_weapons = pd.read_csv("./csvData/weapons.csv")

print(all_weapons.head())

generic_ranged = '''[h:Name="%s"]
[h:type="%s damage"]
[h:dice=%s]
[h:ndice=%s]
[h:attack_bonus=0]
[h:crit_low=%s]
[h:damage_mod=DexMod]
[h:crit_mult=%s]
[h:damage_dice=roll(ndice,dice)]
[h:crit_dice=roll(ndice,dice)]
[h:attack_stat=StrMod]
[h:roll=1d20]

[h:crit_damage=reroll(crit_mult-1, dice+damage_mod, 1+damage_mod)]

[Name]: [roll+attack_stat+BAB-SizeMod+attack_bonus]&lt;br&gt;
[damage_dice+damage_mod] [type]

[if(roll>=crit_low), CODE:{
&lt;br&gt;
Crit chance! [1d20+attack_stat+BAB-SizeMod+attack_bonus] to confirm&lt;br&gt;
[crit_damage] extra damage
};{}]'''

generic_melee = '''[h:Name="%s"]
[h:type="%s damage"]
[h:dice=%s]
[h:ndice=%s]
[h:attack_bonus=0]
[h:crit_low=%s]
[h:damage_mod=StrMod]
[h:crit_mult=%s]
[h:damage_dice=roll(ndice,dice)]
[h:crit_dice=roll(ndice,dice)]
[h:attack_stat=StrMod]
[h:roll=1d20]
[h:crit_damage=reroll(crit_mult-1, dice+damage_mod, 1+damage_mod)]
[Name]: [roll+attack_stat+BAB-SizeMod+attack_bonus] to hit&lt;br&gt;
[damage_dice+damage_mod] [type]

[if(roll>=crit_low), CODE:{
&lt;br&gt;
Crit chance! [1d20+attack_stat+BAB-SizeMod+attack_bonus] to confirm&lt;br&gt;
[crit_damage] extra damage
};{}]

[if(roll == 1),CODE:{
&lt;br&gt;
Critical Fumble!	
	};{}]
'''

ability_dict = {
  "monk":" A monk weapon can be used by a monk to perform a flurry of blows",
  "disarm":"When you use a disarm weapon, you get a +2 bonus on Combat Maneuver Checks to disarm",
  "attached":"",
  "trip":"You can use a trip weapon to make trip attacks. If you are tripped during your own trip attempt, you can drop the weapon to avoid being tripped",
  "reach":"You use a reach weapon to strike opponents 10 feet away, but you can’t use it against an adjacent foe.",
  "grapple":"On a successful critical hit with a weapon of this type, you can grapple the target of the attack.",
  "fragile":"A fragile weapon gains the broken condition if the wielder rolls a natural 1 on an attack roll with the weapon.",
  "brace":"If you use a readied action to set a brace weapon against a charge, you deal double damage on a successful hit against a charging creature",
  "nonlethal":"This weapon deals nonlethal damage",
  "double":"You can use a double weapon to fight as if fighting with two weapons, but if you do, you incur all the normal attack penalties associated with fighting with two weapons",
  "performance":"When wielding this weapon, if an attack or combat maneuver made with this weapon prompts a combat performance check, you gain a +2 bonus on that check.",
  "improvised":"",
  "blocking":"When you use this weapon to fight defensively, you gain a +1 shield bonus to AC",
  "sunder":"When you use a sunder weapon, you get a +2 bonus on Combat Maneuver Checks to sunder attempts.",
  "distracting":"You gain a +2 bonus on Bluff skill checks to feint in combat",
  "deadly":"When you use this weapon to deliver a coup de grace, it gains a +4 bonus to damage when calculating the DC of the Fortitude saving throw"
}

damage_dict = {
  "P":"piercing",
  "S":"slashing",
  "B":"bludgeoning",
  "F":"fire"
}

def parseCritical (critCell):
  returnVal = ["20","2"] #default
  split_cell = critCell.split("/")
  if(len(split_cell) > 1):
    #has a range
    returnVal[0] = split_cell[0]
    returnVal[1] = split_cell[1].replace("x","")
  else:
    returnVal[1] = critCell.replace("x","")
  return returnVal


def parseTypes (specialCell):
  returnValue = [] #default
  if(pd.isna(specialCell)):
    return returnValue
  split_cell = specialCell.split(",")
  for string in split_cell:
    try:
      returnValue.append(ability_dict[string])
    except:
      pass
  return returnValue

melee_weps = all_weapons.loc[all_weapons.Type == "Melee"]
print(melee_weps.head())
def makeCommand(pandasRow):

  file_name = pandasRow.Name.lower()
  label_name = pandasRow.Name.replace("_"," ")
  dmgDiceList = pandasRow.Dmg.split("d")
  criticals = parseCritical(pandasRow.Critical)
  # types = parseTypes(pandasRow.Special)
  types = pandasRow.Special
  template_string = generic_melee
  dmg_type = damage_dict[pandasRow.Type2[0]]
  if(pandasRow.Type == "Ranged"):
    template_string = generic_ranged

  
  commandString = ( template_string % (label_name,dmg_type,dmgDiceList[1],dmgDiceList[0],criticals[0],criticals[1]))
  # print(commandString)
  tool_tip = ""
  if(pd.isna(types) != True):
    tool_tip =  ('Special: %s' % types)
  #not using the map, i like jsut lsuting them

  # for extra in types:
  #   commandString+= ('&lt;br&gt;[s:"Special Qualities: %s"] ' % extra)

  this_macro = Macro(label=label_name, group="Attacks", command=commandString, tooltip=tool_tip)
  this_macro.make_file("./Weapons/output/" + file_name + ".mtmacro")



for index,row in all_weapons.iterrows():
  makeCommand(row)

  

  