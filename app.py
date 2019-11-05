#!/usr/bin/env python3
from user_input import User_input
from retrieve import Retrieve
from plot import Plot

class App:
	#Initializer / instance attributes
	def __init__(self, taxonomy, protein):
		self.Taxonomy = taxonomy
		self.Protein = protein
		self.ncbi_api = Retrieve()
		self.plot = Plot()
		self.dataset = None
	
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

	
	def taxa(self,typ):
		#gets list of all taxa produced from search
		self.dataset = self.ncbi_api.taxa_protein_dict(self.search(),typ)
	

	def search(self):
		#initiates ncbi search using esearch and efetch
		return self.ncbi_api.retrieve(self.protein_query,self.taxon_query)	
