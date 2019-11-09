#!/usr/bin/env python3
from app.spinner import Spinner

class Handler:

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
		user_change = self.ex_check(input("To change an input, enter 1 for taxon, 2 for protein, or 3 for both. otherwise just hit enter to move on.\nValue: "\
			.format(obj.taxon_query,obj.protein_query)))
		if user_change == "1":
			obj.taxon_query = "taxonomy"
		elif user_change == "2":
			obj.protein_query = "protein"
		elif user_change == "3":
			obj.taxon_query = "taxonomy"
			obj.protein_query = "protein"
		elif user_change not in "123" and user_change != "":
			print("Proper inputs would be:\n 1 for taxon, 2 for protein, 3 for both, 'enter' to move on, or 'exit' to exit the program.")
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
			print("Doesn't seem like your taxon choice produced a proper taxon. Try again?")
		else:
			while True:
				print("Taxon query too vague. Narrow down by selecting a number, or enter 0 to choose another taxon or protein:")
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
					print("Make sure your choice is a valid number between 1 and {}, or 0 to exit.".format(len(taxons)))
			return True


	def proceed(self,results):
		if int(results) <= 1:
			print("Sorry, your search produced {} results. That's not enough to continue. Please change a criteria to continue".format(results))
			return False
		ans = self.ex_check(input("your search produced {} results. Enter to proceed: ".format(results)))
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


	@staticmethod
	def display_choices(tax,prot):
		return print("Your inputs were:\n\t1. Taxon: {}\n\t2. Protein: {}\n".format(tax,prot))

