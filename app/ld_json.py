#!/usr/bin/env python3

#JSON file containing all print statements that the program outputs to the screen, this includes
#user input as well potential error messages.
#When passed into a class pulling the error messages, this is passed into the ld_json class which converts
#this json into a dictionary. The dictionary is then passed into another class, such as user_input, handler
#or tools. From there it is filtered for the appropriate outputs by calling Ld_json().class_name.
#From there, each individual error message can be accessed like a normal dictionary.


import json

class Ld_json:
  def __init__(self):
    with open("./app/print_outp.json") as f:
      self.__dict__ = json.load(f)

#test1 = Ld_json().user_input
#print(test1['txid'])
