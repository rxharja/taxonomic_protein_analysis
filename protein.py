#!/usr/bin/env python3
import re

class Protein:
	def __init__(self, protein):
		self.protein = protein


	@classmethod
	def from_input(cls):
		return cls(input("Protein Family: "))		
        

	@property
	def val(self):
		return self.protein

        
	@val.setter
	def val(self,new_protein):
		self.val = new_protein


	def check_input(inp):
		if re.match(".+[0-9]+.+",inp):
			if re.match("txid[0-9]+",inp):
				return False
			else:
				print("It seems like you were attempting to write a taxon ID. the proper format is 'txid' followed by any amount of numbers with no spaces.")
				return True
		if not re.match("^[a-z]*$",inp):
			print("No whitespaces are allowed in your search query.")
			return True
		return False 
