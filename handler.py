#!/usr/bin/env python3
from app import App

def handler(obj):
	input_logic(obj)
	obj.get_summary()
	if proceed(obj.summary):
		print("end of script")
		return None
	else:
		return handler(obj) 
		
def input_logic(obj):
	while True:
		if input_handler(obj):
			if taxon_handler(obj):
				break		

def input_handler(obj):
	display_choices(obj.taxon_query,obj.protein_query)
	user_change = ex_check(input("To change an input, enter 1 for taxon, 2 for protein, or 3 for both. otherwise just hit enter to move on.\nValue: "\
		.format(obj.taxon_query,obj.protein_query)))
	if user_change == "1":
		obj.taxon_query = "taxonomy"
	elif user_change == "2":
		obj.protein_query = "protein"
	elif user_change == "3":
		#obj.taxon_query = "taxonomy"
		#obj.protein_query = "protein"
		obj.from_class()
	elif user_change not in "123" and user_change != "":
		print("Proper inputs would be:\n 1 for taxon, 2 for protein, 3 for both, 'enter' to move on, or 'exit' to exit the program.")
	if user_change == "":
		return True
	return False

def taxon_handler(obj):
	print("Checking taxon choice, please wait...")
	taxons = obj.get_taxa()
	if len(taxons) == 1:
		return True;
	else:
		while True:
			print("Taxon query too vague. Narrow down by selecting a number, or enter 0 to choose another taxon or protein:")
			[print("{}. {}".format(i+1,taxons[i])) for i in range(len(taxons))]
			try:
				inp = int(ex_check(input("Choice :")))
				if inp == 0:
					return False
				inp -= 1
				choice = taxons[inp][0:taxons[inp].find(':')]
				obj.taxon_query = choice
				display_choices(obj.taxon_query,obj.protein_query)
				break
			except:
				print("Make sure your choice is a valid number between 1 and {}, or 0 to exit.".format(len(taxons)))
		return True

def proceed(results):
	ans = ex_check(input("your search produced {} results. Proceed?(y/n): ".format(results)))
	if ans == "y":
		return True
	else:
		return False


def ex_check(inp):
	if inp == "exit":
		exit()
	return inp


def display_choices(tax,prot):
	return print("Your inputs were:\n\t1. Taxon: {}\n\t2. Protein: {}\n".format(tax,prot))

app = App.from_class()
handler(app)
