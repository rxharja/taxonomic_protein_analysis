#!/usr/bin/env python3
import json

class Ld_json:
  def __init__(self):
    with open("./app/print_outp.json") as f:
      self.__dict__ = json.load(f)

#test1 = Ld_json().user_input
#print(test1['txid'])
