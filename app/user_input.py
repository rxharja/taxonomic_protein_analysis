#!/usr/bin/env python3
import re
from app.ld_json import Ld_json

#class handling user input for assigning of the taxon and protein query values
class User_input:
  #import our print statements to display to the user from our json file
  out = Ld_json().user_input


  #initialize our user_input value and whatever parameter (protein or taxon) was used to make this class
  def __init__(self, user_input, param):
    self.user_input = user_input
    self.param = param


  #direct assigning of variables to class without asking for user input, just using equal signs
  @classmethod
  def from_param(cls,itm,param):
    return cls(itm,param)


  #this one is the same as above but it takes a user input. There is an error trap if a developer tries to pass in a a parameter that doesnt work, only taxon and protein work
  @classmethod
  def from_input(cls, param):
    if param == "taxonomy":
      txt = "Taxonomic Group: "
    elif param == "protein":
      txt = "Protein family: "
    else:
      print(cls.out['param_error'])
      exit()
    inp = input(txt)
    inp = inp.lower()
    #a return of true will keep looping until check_input accepts the input as appropriate, inp stops being reassigned at that point and gets passed into the class
    while cls.check_input(cls.out,param,inp):
      inp = input(txt)
    return cls(inp,param)


  #this method handles checking the user input with regular expressions to make sure that they conform to program standards, like no spaces in protein names, no empty spaces in general, no adding txid or uid because thats something I handle in the retrieve class, and of course , feedback for the user to let them know what they're doing wrong.  
  @staticmethod  
  def check_input(out,param,inp):
    #exit conditions
    exits = ['exit','q','quit']
    if inp in exits: exit()i
    #handle empty inputs as not acceptable
    if inp.strip() == "":
      print(out['no_input'])  
      return True 
    if param == "taxonomy": #taxonomy checks
      if re.match(".*[0-9]+.*",inp): #if theres numbers, find out if txid or uid in there, then tell user to change that
        if re.match("txid[0-9]+",inp):
          print(out['txid'])
          return True
        elif re.match("[0-9]+\[uid\]",inp):
          print(out['uid'])
        elif re.match("[0-9]+",inp): #let it pass if its just numbers
          return False
        else:#no alphanumeric 
          #print(out['alphanumeric']) #initially didnt accept spaces in taxon query but then i remembred thats a common feature
          return True
      if not re.match("^[a-z]*$",inp):
        print(out['whitespace'])
        return True
      return False
    else:#protein checks, we just check to make sure it matches this format, spaces aren't allowed
      if re.match("^[a-z]+[a-z0-9-_]*[a-z0-9]$",inp):
        return False
      else:
        print(out['protein'])
        return False
