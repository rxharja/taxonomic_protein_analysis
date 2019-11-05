#!/usr/bin/env python3
from user_input import User_input
from retrieve import Retrieve

class App:
	#Initializer / instance attributes
	def __init__(self, taxonomy, protein):
		self.Taxonomy = taxonomy
		self.Protein = protein
		self.ncbi_api = Retrieve()
	
	@classmethod
	def from_class(cls):
		return cls(User_input.from_input("taxonomy"),
			   User_input.from_input("protein")
		)


	@property
	def taxon_query(self):
		return self.Taxonomy.val


	@taxon_query.setter
	def taxon_query(self,inp):
		self.Taxonomy = User_input.from_input(inp)
 

	@property
	def protein_query(self):
		return self.Protein.val


	@protein_query.setter
	def protein_query(self,inp):
		self.Protein = User_input.from_input(inp)

	
	def taxa(self):
		return self.ncbi_api.taxa(self.search())
	

	def search(self):
		return self.ncbi_api.retrieve(self.protein_query,self.taxon_query)	
