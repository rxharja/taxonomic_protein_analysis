#!/usr/bin/env python3
import subprocess,os

class Tools:

	def __init__(self):
		self.fasta = None
		self.alignment_file = None
		self.consensus = None
		self.db = None
		self.blast = None
		if not os.path.isdir("./outputs"):
			os.mkdir("./outputs")
	

	@staticmethod
	def check_file(*argv):
		bools = []
		for arg in argv:
			bools += [os.path.isfile(arg)]
		if False in bools:
			return False
		return True	


	@staticmethod
	def run(inp):
		return subprocess.check_output(inp,shell=True)


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
		if self.check_file(self.fasta):
			self.alignment_file = title
			self.run("clustalo -i {} -t protein -o {} --force".format(self.fasta,title))
		else:
			print("fasta file needed for clustalo alignment.")
			exit()


	def cons(self,title="./outputs/consensus.fasta"):
		if self.check_file(self.fasta):
			self.consensus = title
			self.run("cons -sprotein1 {} -outseq {}".format(self.alignment_file,title))
		else:
			print("Fasta file not generated, please generate fasta file first")
			exit()
	
	
	def blast(self,db_title="./outputs/output_db",b_file="./outputs/blastp.out"):
		if self.check_file(self.consensus,self.fasta):
			self.run("makeblastdb -in {} -dbtype prot -out {}".format(self.fasta,db_title))
			self.db = db_title
			self.run("blastp -db {} -query {} -outfmt 6 > {}".format(self.db,self.consensus,b_file))
			self.blast = b_file
		else:
			print("Consensus sequence needs to generated from align method, and fasta file must be available")


	def plot(self):
		return None

	
	def filter(self,max_seq):
		counter = 0
		outf = "./outputs/list_{}.txt".format(max_seq)
		with open(self.blast,'r') as bf: 
			with open(outf,"a") as out:
				for line in bf:
					counter += 1
					out.write(line.split()[1])

		self.run("/localdisk/data/BPSM/Assignment2/pullseq -i {} -n {} > {}".format(self.fasta,outf,"filtered.fasta"))
