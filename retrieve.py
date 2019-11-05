#!usr/bin/env python3
import subprocess,re

class Retrieve():
	
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


	def retrieve(self,protein,taxon,db="Protein",form="fasta"):
		#returns fasta file given search parameters
		outp = subprocess.check_output("esearch -db {} -query '{}[organism] AND {}[Protein] NOT PARTIAL NOT PREDICTED' | efetch -db {} -format {}".format(db,taxon,protein,db,form),shell=True)
		return outp.decode("utf-8")

