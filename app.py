#!/usr/bin/env python3
import subprocess
from protein import Protein
from taxonomy import Taxonomy

class App:
	#Initializer / instance attributes
	def __init__(self):
		self.taxonomy = Taxonomy.from_input()
		self.protein = Protein.from_input()


	def retrieve(self,db="Protein",form="acc"):
		subprocess.call( "esearch -db {} -query '{}[organism] AND {}[Protein]' | efetch -db {} -format {}".
			format(db,self.taxonomy.val,self.protein.val,db,form) , shell = True )

app = App()
app.retrieve()
