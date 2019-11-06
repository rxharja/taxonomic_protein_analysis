#!/usr/bin/env python3
from app import App


def handler():
	app = App.from_class()
	while taxon_handler(app):
		continue
	while True:
		input_handler(app)
		app.get_summary()
		if proceed(app.summary):
			break
	

def input_handler(obj):
	user_change = input("Your inputs were:\n\t1. Taxon: {}\n\t2. Protein: {}\nIf you wish to change one of your inputs, enter 1 for taxon, 2 for protein, or 3 for both. otherwise just hit enter to move on.\nValue: "\
		.format(obj.taxon_query,obj.protein_query))
	if user_change == "1":
		obj.taxon_query = "taxonomy"
	elif user_change == "2":
		obj.protein_query = "protein"
	elif user_change == "3":
		obj.taxon_query = "taxonomy"
		obj.protein_query = "protein"
	elif user_change == "4" or user_change == "exit":
		print("Exiting program")
		exit()
	if user_change in "123" and user_change != "":
		proceed = input("\nYour new values are:\n1. Taxon: {}\n2. Protein: {}\nAre you happy with this?(y to proceed): ".format(obj.taxon_query,obj.protein_query))
		if proceed.lower() != "y":
			input_handler(obj)

def taxon_handler(obj):
	#TODO: return bool true once taxon list is just 1, else return false
	if len(obj.get_taxa) == 1:
		return False;
	else:
		#TODO: Print out list of taxa to choose from
		#TODO: allow user to choose one and pass input to obj.taxon_query
def proceed(results):
	ans = input("your search produced {} results. Proceed?(y/n)".format(results))
	if ans == "y":
		return True
	else:
		return False

handler()
