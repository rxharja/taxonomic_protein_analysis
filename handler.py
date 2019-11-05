#!/usr/bin/env python3
from app import App


def handler():
	app = App.from_class()
	while True:
		input_handler(app)
		app.taxa(typ="accessions")
		if proceed(len(app.dataset),sum(len(val) for val in app.dataset.values())):
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
	if user_change in "123" and user_change != "":
		proceed = input("\nYour new values are:\n1. Taxon: {}\n2. Protein: {}\nAre you happy with this?(y to proceed): ".format(obj.taxon_query,obj.protein_query))
		if proceed.lower() != "y":
			input_handler(obj)


def proceed(species,proteins):
	ans = input("your results produced:\n{} for species\n{} for proteins. Proceed?(y/n)".format(species,proteins).lower())
	if ans == "y":
		return True
	else:
		return False

handler()
