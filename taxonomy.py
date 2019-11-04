#!/usr/bin/env python3
import re

class Taxonomy:
	def __init__(self, taxonomy):
		self.taxonomy = taxonomy


	@classmethod
	def from_input(cls):
		inp = input("Taxonomic Group: ")
		while cls.check_input(inp):
			inp = input("Taxonomic Group: ")
		return cls(inp.lower())

        
	@property
	def val(self):
		return self.taxonomy

        
	@val.setter
	def val(self,new_taxonomy):
		self.taxonomy = new_taxonomy

	
	def check_input(inp):
		#todo: check for numbers, then if true, check if in txid#### format
		#else, check for any strange characters like whitespaces
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
