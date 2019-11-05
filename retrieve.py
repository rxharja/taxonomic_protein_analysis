#!usr/bin/env python3
import subprocess,re

class Retrieve():
	def __init__(self):
		self.num_species = None
		self.num_hits = None
	
	def taxa_protein_dict(self,f):
		#returns list of all taxa from fasta file
		#species = [itm.replace("[","").replace("]","") for itm in re.findall(r"\[.*\]",f)]
		#return species

	def proteins(self,f):
		#returns list of all proteins from fasta file
		return None


	def retrieve(self,protein,taxon,db="Protein",form="fasta"):
		#returns fasta file given search parameters
		print("Retrieving protein {} from taxon {} in {} format, please wait...".format(protein,taxon,form))
		outp = subprocess.check_output("esearch -db {} -query '{}[organism] AND {}[Protein] NOT PARTIAL' | efetch -db {} -format {}".format(db,taxon,protein,db,form),shell=True)
		return outp.decode("utf-8")

