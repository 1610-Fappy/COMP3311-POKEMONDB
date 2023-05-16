# COMP3311 23T1 Assignment 2 ... Python helper functions
# add any functions to share between Python scripts
# Note: you must submit this file even if you add nothing to it

import re
import math

def clean(s: str) -> str:
    """
    Clean user input
    remove leading and trailing whitespace
    convert to title case (first letter of each word is uppercase, the rest are lowercase)
    squish multiple whitespace characters into a single space
    """
    return re.sub(r'\s+', ' ', s.strip().title())


# Function to calculate damage of each move on defending pokemon
""" Inputs:
        List of (attack,defending) type effectiveness tuples 
        List of effectiveness multipliers corresponding to each tuple in above list    
        List of attack_move tuples same form as tuples from query for attacking moves
        Defender tuple containing defender details

"""
def calcdmg(attkList,multList, moveList : list, defender):
    # Initialising variables to be used in loop
    outlist = []
    minrand = 0.85
    minlvl = 1
    maxlvl = 100
    maxrand = 1.0
    mindmg = 0
    maxdmg = 0
    alignval = 0
    alignmin = 0
    alignmax = 0
    # Extracing stats for attacker special, normal and defender special,normal
    defendspec = int(defender[3].split(',')[4])
    defendnorm = int(defender[3].split(',')[2])
    attkspec = int(moveList[0][5].split(',')[3])
    attknorm = int(moveList[0][5].split(',')[1])
    for t in moveList:
        typeEffec = 1.0;
        stab = 1.0
        power = t[1]
        if(t[6] == 'Special'):
            A = attkspec
            D = defendspec
        else:
            A = attknorm
            D = defendnorm
        if (t[3] == t[2]):
            stab = 1.5
        if(t[4] is not None and t[4] == t[2]):
            stab = 1.5
        if ((t[2],defender[1]) in attkList):
    	    typeEffec = typeEffec * multList[attkList.index((t[2],defender[1]))]/100.0
    	   
        if (defender[2] is not None and (t[2],defender[2]) in attkList):
            typeEffec = typeEffec * multList[attkList.index((t[2],defender[2]))]/100.0
        mindmg = (((((2 * minlvl)/5.0)+2.0)*power*(A/D))/50.0 + 2.0)*minrand*stab*typeEffec
        maxdmg = (((((2 * maxlvl)/5.0)+2.0)*power*(A/D))/50.0 + 2.0)*maxrand*stab*typeEffec

        mindmg = math.trunc(round(mindmg,1))
        maxdmg = math.trunc(round(maxdmg,1))

        if (maxdmg == 0):
            continue
        
        # Conditions to get appropriate align value for formatting output
        if (len(t[0]) > alignval):
            alignval = len(t[0])
        if (len(str(round(t[1]))) > alignmin):
            alignmin = len(str(t[1]))
        if (len(str(round(t[2]))) > alignmax):
            alignmax = len(str(t[2]))
        if (maxdmg != 0):
            outlist.append((t[0],mindmg,maxdmg))
    
    return outlist, alignval,alignmin,alignmax

def invertReqs (tup):
    if(tup[7] is True):
        newreq = 'NOT' + tup[8]
    else:
        newreq = tup[8]
    
    return newreq

def inv_req(tup_list : list):
    if (len(tup_list) == 0):
        return tup_list
    new_list = []
    new_req = ''
    for t in tup_list:
        if (t[3] is True):
            new_req = 'NOT ' + t[4]
        else:
            new_req = t[4]
        new_list.append((t[0],t[1],t[2],new_req))

    return new_list

def pre_post_split(tup_list : list, poke_id):
    if (len(tup_list) == 0):
        return tup_list
    pre_list = []
    post_list = []

    for t in tup_list:
        if (t[2] == poke_id):
            pre_list.append((t[0],t[1],t[3],t[5], t[6]))
        else:
            post_list.append((t[0],t[2],t[4],t[5],t[6]))
    
    return pre_list, post_list


def split_tup_vals(tup_list : list):
    if (len(tup_list) == 0):
        return tup_list
    evonum_list = []
    name_list = []
    req_list = []

    for t in tup_list:
        evonum_list.append(t[0])
        name_list.append(t[2])
        req_list.append(t[3])

    return evonum_list, name_list, req_list

def split_post(tup_list : list):
    if (len(tup_list) == 0):
        return tup_list
    evonum_list, name_list, req_list = split_tup_vals(tup_list)

    new_list = []
    inside_list = []
    for i,t in enumerate(tup_list):
        if (name_list[i] != name_list[i-1] and i != 0):
            new_list.append(inside_list)
            inside_list = []
        elif (name_list[i] == name_list[i-1] or i == 0):
            inside_list.append(t)
        if (inside_list == []):
            inside_list.append(t)
        if (i == len(tup_list) - 1):
            new_list.append(inside_list)

    return new_list

def calc_scaleDens(height, weight, rarity):
    volume = (4.0/3.0) * math.pi * (height*0.5*100)**3
    density = (weight*1000) / volume
    scaledDens = density * (rarity*0.01)
    return scaledDens

def print_types(typeList : list, first_type, second_type):

    if(second_type is None):
        print(f"\t\tType: {typeList[first_type]}")
    else:
        print(f"\t\tType: {typeList[first_type]}/{typeList[second_type]}")
    return

def level_split(Stringtuple):
    res = Stringtuple.split(',')
    print(f"\t\tLevels: min {res[0][1:]}, max {res[1][:-1]}")

def requirements_out(eggList : list, poke_list : list, poke_name):

    print("\t\tEncounter Requirements:")
    egg_index = poke_list.index(poke_name)

    for t in eggList[egg_index]:
        print(f"\t\t\t{t}")

    return

def egg_out(eggList : list, poke_list : list, poke_name):

    egg_index = -1
    if (poke_name in poke_list):
        egg_index = poke_list.index(poke_name)

    if (egg_index != -1 and eggList != []):
        print(f"\t\tEgg Groups: {', '.join(eggList[egg_index])}")

    return

def abil_out(eggList : list, poke_list : list, poke_name):

    egg_index = -1
    if (poke_name in poke_list):
        egg_index = poke_list.index(poke_name)

    if (egg_index != -1 and eggList != []):
        print(f"\t\tAbilities: {', '.join(eggList[egg_index])}")

    return

def output_format_post(tup_list : list):

    evonum_list, name_list, req_list = split_tup_vals(tup_list)

    outstring = ''
    sixtab = False
    fourtab = False
    for i,value in enumerate(tup_list):
        if (i == 0 ):
            outstring = outstring + '\t' + f"'{name_list[i]}' when the following requirements are satisfied:\n"  
        if (i != 0 and evonum_list[i] == evonum_list[i-1]):
            if (sixtab):
                outstring = outstring + '\n' + '\t\t\t' + 'AND\n'
                sixtab = False
            elif (fourtab):
                outstring = outstring + '\n' + '\t\t' + 'AND\n'
                fourtab = False
        elif (i != 0 and evonum_list[i] != evonum_list[i-1]):
            outstring = outstring + '\n' + '\t\t' + 'OR\n'

        if (evonum_list.count(evonum_list[i]) != len(evonum_list) and evonum_list.count(evonum_list[i]) > 1):
            outstring = outstring + '\t\t\t\t' + req_list[i]
            sixtab = True
        elif (evonum_list.count(evonum_list[i]) != len(evonum_list) and evonum_list.count(evonum_list[i]) == 1):
            outstring =  outstring + '\t\t\t' + req_list[i]           
        elif (evonum_list.count(evonum_list[i]) == len(evonum_list) and evonum_list.count(evonum_list[i]) > 1):
            outstring =  outstring + '\t\t\t' + req_list[i]
            fourtab = True
        elif (evonum_list.count(evonum_list[i]) == len(evonum_list) and evonum_list.count(evonum_list[i]) == 1):
            outstring =  outstring + '\t\t' + req_list[i]

    return outstring
                        

def output_format(tup_list : list):

    evonum_list, name_list, req_list = split_tup_vals(tup_list)

    outstring = ''
    sixtab = False
    fourtab = False
    for i,value in enumerate(tup_list):
        if (i != 0 and evonum_list[i] == evonum_list[i-1]):
            if (sixtab):
                outstring = outstring + '\n' + '\t\t\t' + 'AND\n'
                sixtab = False
            elif (fourtab):
                outstring = outstring + '\n' + '\t\t' + 'AND\n'
                fourtab = False
        elif (i != 0 and evonum_list[i] != evonum_list[i-1]):
            outstring = outstring + '\n' + '\t\t' + 'OR\n'

        if (evonum_list.count(evonum_list[i]) != len(evonum_list) and evonum_list.count(evonum_list[i]) > 1):
            outstring = outstring + '\t\t\t\t' + req_list[i]
            sixtab = True
        elif (evonum_list.count(evonum_list[i]) != len(evonum_list) and evonum_list.count(evonum_list[i]) == 1):
            outstring =  outstring + '\t\t\t' + req_list[i]           
        elif (evonum_list.count(evonum_list[i]) == len(evonum_list) and evonum_list.count(evonum_list[i]) > 1):
            outstring =  outstring + '\t\t\t' + req_list[i]
            fourtab = True
        elif (evonum_list.count(evonum_list[i]) == len(evonum_list) and evonum_list.count(evonum_list[i]) == 1):
            outstring =  outstring + '\t\t' + req_list[i]

    return outstring
                        
