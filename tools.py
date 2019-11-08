#!/usr/bin/env python3
import subprocess,os

class Tools:

	def __init__(self):
		self.fasta = None
		self.alignment_file = None
		if not os.path.isdir("./outputs"):
			os.mkdir("./outputs")


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
		if self.fasta:
			self.alignment_file = title
			return self.run("clustalo -i {} -o {}".format(self.fasta,title))
		print("fasta file needed for clustalo alignment.")
		exit()


	def cons(self,title="./outputs/consensus.fasta"):
		if self.fasta:
			return self.run("cons {} {}".format(self.alignment_file,title))
		print("Fasta file not generated, please generate fasta file first")
		exit()
	

		
	def plot(self):
		self.align()
		self.cons()
