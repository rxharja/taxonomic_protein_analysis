#!/usr/bin/env python3
#import user_input, retrieve, and plot classes and abstract them
#this class is the main interface for handler.py to control the flow
#of the application.
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
		self.fasta = None
		self.summary = None
	
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
		if inp != "taxonomy":
			self.Taxonomy = User_input.from_param(inp,"taxonomy")
		else:
			self.Taxonomy = User_input.from_input("taxonomy")
 

	@property
	def protein_query(self):
		return self.Protein.val


	@protein_query.setter
	def protein_query(self,inp):
		self.Protein = User_input.from_input("protein")
	

	def get_taxa(self):
		#given self.taxon_query, return list of
		return self.ncbi_api.get_taxa(self.taxon_query)
 

	def taxa(self,typ):
	#	gets list of all taxa produced from search
		self.dataset = self.ncbi_api.taxa_protein_dict(self.search(),typ)
	

	def get_summary(self):
		self.summary = self.ncbi_api.summary(self.protein_query,self.taxon_query)


	def get_fasta(self):
		#initiates ncbi search using esearch and efetch
		self.fasta = self.ncbi_api.retrieve(self.protein_query,self.taxon_query)
		return self.fasta
