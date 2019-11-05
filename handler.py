#!/usr/bin/env python3
from app import App


def handler(obj):
	user_change = input("Your inputs were:\n\t1. Taxon: {}\n\t2. Protein: {}\nIf you wish to change one of your inputs, enter 1 for taxon, 2 for protein, or 3 for both. otherwise just hit enter to move on.\nValue: "\
		.format(obj.taxon_query,obj.protein_query))
	if user_change == "1":
		obj.taxon = "taxonomy"
	elif user_change == "2":
		obj.protein = "protein"
	elif user_change == "3":
		obj.taxon = "taxonomy"
		obj.protein = "protein"
	if user_change in "123" and user_change != "":
		proceed = input("\nYour new values are:\n1. Taxon: {}\n2. Protein: {}\nAre you happy with this?(y to proceed): ".format(obj.taxon,obj.protein))
		if proceed.lower() != "y":
			handler(obj)

app = App.from_class()
handler(app)
print(app.taxa())     
