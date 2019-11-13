#!/usr/bin/env python3
import re
from app.ld_json import Ld_json

class User_input:
  out = Ld_json().user_input

  def __init__(self, user_input, param):
    self.user_input = user_input
    self.param = param


  @classmethod
  def from_param(cls,itm,param):
    return cls(itm,param)


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
    while cls.check_input(cls.out,param,inp):
      inp = input(txt)
    return cls(inp,param)

        
  @property
  def val(self):
    return self.user_input

        
  @val.setter
  def val(self,new_input):
    self.user_input = new_input


  @staticmethod  
  def check_input(out,param,inp):
    exits = ['exit','q','quit']
    if inp in exits: exit()
    if inp.strip() == "":
      print(out['no_input'])  
      return True
    if param == "taxonomy":
      if re.match(".*[0-9]+.*",inp):
        if re.match("txid[0-9]+",inp):
          print(out['txid'])
          return True
        elif re.match("[0-9]+\[uid\]",inp):
          print(out['uid'])
        elif re.match("[0-9]+",inp):
          return False
        else:
          print(out['alphanumeric'])
          return True
      if not re.match("^[a-z]*$",inp):
        print(out['whitespace'])
        return True
      return False
    else:
      if re.match("^[a-z]+[a-z0-9-_]*[a-z0-9]$",inp):
        return False
      else:
        print(out['protein'])
        return False
