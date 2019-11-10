#!/usr/bin/env python3
import subprocess,os
from app.ld_json import Ld_json

class Tools:
	out = Ld_json().tools

	def __init__(self):
		#store pathways of each file as they're generated as strings
		#Make output directory if it does not exist upon initialising
		self.fasta = None
		self.alignment_file = None
		self.consensus = None
		self.db = None
		self.blast_file = None
		if not os.path.isdir("./outputs"):
			os.mkdir("./outputs")
	

	@staticmethod
	def check_file(*argv):
		#takes each file passed into function as a list, 
		#evaluates if they exist and appends them to a list
		#If they all exist, returns true, otherwise false.
		bools = []
		for arg in argv:
			bools += [os.path.isfile(arg)]
		if False in bools:
			return False
		return True	


	@staticmethod
	def run(inp):
		#Just made it easier to run suprocess.call to shell
		return subprocess.call(inp,shell=True)


	def write(self,inp_f,p="protein",t="taxon",alt=""):
		p = p.replace(" ","_")
		title = "./outputs/"
		if alt == "":
			title +="{}_{}.fasta".format(t,p)
		else:
			title += alt
		self.fasta = title
		f = open(title,"w")
		f.write(inp_f)


	def align(self,title="./outputs/alignment.out"):
		#calls clustalo to align the fasta file 
		#outputs it to default alignment,out in outputs
		if self.check_file(self.fasta):
			self.alignment_file = title
			self.run("clustalo -i {} -t protein -o {} --force".format(self.fasta,title))
		else:
			print(self.out['alignment_err'])
			exit()


	def cons(self,title="./outputs/consensus.fasta"):
		#calls cons from emboss tools to create a conensus sequence
		#of our aligned sequences, outputs as default consensus.fasta
		#to outputs folder
		if self.check_file(self.fasta):
			self.consensus = title
			self.run("cons -sprotein1 {} -outseq {}".format(self.alignment_file,title))
		else:
			print(self.out['consensus_err'])
			exit()
	
	
	def blast(self,db_file="./outputs/output_db",b_file="./outputs/blastp.out"):
		#runs two processes, first creates a blast databae given fasta file to output_db
		if self.check_file(self.consensus,self.fasta):
			self.run("makeblastdb -in {} -dbtype prot -out {}".format(self.fasta,db_file))
			self.db = db_file
			self.run("blastp -db {} -query {} -outfmt 6 > {}".format(self.db,self.consensus,b_file))
			self.blast_file = b_file
		else:
			print(self.out['blast_err'])


	#def plot(self):
	#	return None

	
	def filter(self,max_seq):
		counter = 0
		outf = "./outputs/list_{}.txt".format(max_seq)
		filtered = "./outputs/top{}_filtered.fasta"
		with open(self.blast_file,'r') as bf: 
			with open(outf,"a") as out:
				for line in bf:
					counter += 1
					out.write(line.split()[1]+"\n")

		self.run("/localdisk/data/BPSM/Assignment2/pullseq -i {} -n {} > {}".format(self.fasta,outf,filtered))
