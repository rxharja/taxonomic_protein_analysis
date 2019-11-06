#!/usr/bin/env python3
import re

class User_input:
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
			print("invalid param value, only taxonomy or protein allowed")
			exit()
		inp = input(txt)
		inp = inp.lower()
		while cls.check_input(param,inp):
			inp = input(txt)
		return cls(inp,param)

        
	@property
	def val(self):
		return self.user_input

        
	@val.setter
	def val(self,new_input):
		self.user_input = new_input

	
	@staticmethod
	def check_input(param,inp):
		if inp == "exit":
			exit()
		if param == "taxonomy":
			if re.match(".*[0-9]+.*",inp):
				if re.match("txid[0-9]+",inp):
					return False
				else:
					print("It seems like you were attempting to write a taxon ID. the proper format is 'txid' followed by any amount of numbers with no spaces.")
					return True
			if not re.match("^[a-z]*$",inp):
				print("No whitespaces are allowed in your search query.")
				return True
			return False
		else:
			if re.match("^[a-z]+[a-z0-9-_]*[a-z0-9]$",inp):
				return False
			else:
				print("Invalid protein name, make sure there are no spaces.")
				return False
