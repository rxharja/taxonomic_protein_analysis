#!/usr/bin/env python3
from app.spinner import Spinner
from app.ld_json import Ld_json

class Handler:
	out = Ld_json().handler

	def __init__(self):
		self.taxon_cache = {}
		self.protein_cache = [
]

	def input_logic(self,obj):
		while True:
			if self.input_handler(obj):
				if self.taxon_handler(obj):
					break		


	def input_handler(self,obj):
		self.display_choices(obj.taxon_query,obj.protein_query)
		user_change = self.ex_check(input(self.out['user_change']).format(obj.taxon_query,obj.protein_query))
		if user_change == "1":
			obj.taxon_query = "taxonomy"
		elif user_change == "2":
			obj.protein_query = "protein"
		elif user_change == "3":
			obj.taxon_query = "taxonomy"
			obj.protein_query = "protein"
		elif user_change not in "123" and user_change != "":
			print(self.out['improper_input'])
		if user_change == "":
			return True
		return False


	def taxon_handler(self,obj):
		try:
			taxons = self.taxon_cache[obj.taxon_query]	
		except:
			with Spinner("Checking taxon choice, please wait "): taxons = obj.get_taxa()
			self.taxon_cache[obj.taxon_query] = taxons
		if len(taxons) == 1:
			return True
		if len(taxons) == 0:
			print(self.out['no_taxons'])
		else:
			while True:
				print(self.out['vague_taxons'])
				[print("{}. {}".format(i+1,taxons[i])) for i in range(len(taxons))]
				try:
					inp = int(self.ex_check(input("Choice :")))
					if inp == 0:
						return False
					inp -= 1
					choice = taxons[inp][0:taxons[inp].find(':')]
					obj.taxon_query = choice
					self.display_choices(obj.taxon_query,obj.protein_query)
					break
				except:
					print(self.out['improper_choice'].format(len(taxons)))
			return True


	def proceed(self,results):
		if int(results) <= 1:
			print(self.out['no_results'].format(results))
			return False
		ans = self.ex_check(input(self.out['results'].format(results)))
		if ans == "":
			return True
		else:
			print("Returning")
			return False


	@staticmethod
	def ex_check(inp):
		exits = ['exit','quit','q']
		if inp in exits:
			exit()
		return inp


	def display_choices(self,tax,prot):
		return print(self.out['display'].format(tax,prot))

