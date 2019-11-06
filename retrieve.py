#!usr/bin/env python3
import subprocess,re
#retrieve class uses subprocess to call esearch and efetch to generate a fasta file given a protein and taxon.
#The fasta file is processed into a dictionary of accessions/protein sequences per species

class Retrieve():
	def __init__(self):
		self.fasta = None

	
	def taxa_protein_dict(self,f,typ="proteins"):
		#returns list of all taxa from fasta files
		t_p_dict = {}
		species = [itm.replace("[","").replace("]","") for itm in re.findall(r"\[.*\]",f)]
		def build_dict(itr):
			for i in range(len(species)):
				try:
					t_p_dict[species[i]] += [itr[i]]
				except:
					t_p_dict[species[i]] = [itr[i]]
		if typ == "accessions":
			accessions = [itm for itm in re.findall(r"[A-Z]+_?\d+\.\d",f)]
			build_dict(accessions)
		elif typ == "proteins":
			proteins = re.split(r">.{0,150}]",f.replace("\n",""))
			proteins = list(filter(None,proteins))
			build_dict(proteins)
		return t_p_dict
	

	def get_taxa(self, taxon, db="Taxonomy"):
		if re.match("[0-9]+",taxon):
			taxon = taxon+"[UID]"
		tax = subprocess.check_output("esearch -db {} -query {} | efetch -format txt".format(db,taxon),shell=True)		
		tax = tax.decode("utf-8").replace("    ",": ").replace("\n","")
		tax = re.split(r"\d\. ",tax)
		tax = list(filter(None,tax))
		return tax


	def summary(self, protein,taxon,db="Protein"):
		if re.match("[0-9]+",taxon):
			taxon = "txid"+taxon
		outp = subprocess.check_output("esearch -db {} -query '{}[organism] AND {}[Protein] NOT PARTIAL NOT PREDICTED'".format(db,taxon,protein),shell=True)
		outp = outp.decode("utf-8")
		return re.findall(r"<Count>.*</Count>",outp)[0].replace("<Count>","").replace("</Count>","")


	def retrieve(self,protein,taxon,db="Protein",form="fasta"):
		#returns fasta file given search parameters
		if re.match("[0-9]+",taxon):
			taxon = "txid"+taxon
		outp = subprocess.check_output("esearch -db {} -query '{}[organism] AND {}[Protein] NOT PARTIAL NOT PREDICTED' | efetch -db {} -format {}".format(db,taxon,protein,db,form),shell=True)
		self.fasta = outp.decode("utf-8")
		return outp.decode("utf-8")

