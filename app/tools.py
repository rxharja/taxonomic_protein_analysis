#!/usr/bin/env python4
import subprocess,os
from app.ld_json import Ld_json
from app.splitter import Splitter

class Tools:
  out = Ld_json().tools

  def __init__(self,path="./outputs/"):
    #store pathways of each file as they're generated as strings
    #Make output directory if it does not exist upon initialising
    if not os.path.isdir(path): os.mkdir(path)
    self.fasta = None
    self.alignment_file = None
    self.consensus = None
    self.db = None
    self.blast_file = None
    self.top_250 = None
    self.list_of_acc = None
    self.path = path
    self.splitter = Splitter()


  @staticmethod  
  def remove_spaces(s):
    return  s.replace(" ","_")


  @staticmethod
  def throw_err(outp):
    print(outp)
    exit()


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
    t = t.replace(" ","_")
    title = self.path
    if alt == "":
      title +="{}_{}_accs.fasta".format(t,p)
    else:
      title += alt
    self.list_of_acc = title
    with open(title,"w+") as f:
      for species in inp_f.keys():
        for acc in inp_f[species].keys():
          f.write(acc+"\n")


  def align(self,fasta,title="alignment.fasta"):
    #calls clustalo to align the fasta file 
    #outputs it to default alignment,out in outputs
    title = self.path + title.replace(" ","_")
    self.fasta = fasta
    if self.check_file(self.fasta):
      self.alignment_file = title
      self.run("clustalo -i {} -t protein --force -o {}".format(self.fasta,title))
    else:
      self.throw_err(self.out['alignment_err'])


  def cons(self,title="consensus.fasta"):
    #calls cons from emboss tools to create a conensus sequence
    #of our aligned sequences, outputs as default consensus.fasta
    #to outputs folder
    title = self.path + title.replace(" ","_")
    if self.check_file(self.fasta):
      self.consensus = title
      self.run("cons -sprotein1 {} -outseq {} -auto Y".format(self.alignment_file,title))
    else:
      self.throw_err(self.out['consensus_err'])  
  

  def blast(self,db_file="output_db",b_file="blastp.out"):
    #runs two processes, first creates a blast database given fasta file to output_db
    if self.check_file(self.consensus,self.fasta):
      db_file = self.path + db_file
      b_file = self.path + b_file
      self.run("makeblastdb -in {} -dbtype prot -out {}".format(self.fasta,db_file))
      self.db = db_file
      self.run("blastp -db {} -query {} -max_hsps 1 -outfmt 6 > {}"\
      .format(self.db,self.consensus,b_file))
      self.blast_file = b_file
    else:
      self.throw_err(self.out['blast_err'])


  def plot(self,algn_file="",winsize='4',graph='svg',title="plotcon"):
    if not algn_file:
      if self.alignment_file:
        algn_file = self.alignment_file
      else:
        self.throw_err(self.out['plot_err'])
    title = title.replace(" ","_")
    self.run("plotcon {} -winsize {} -graph {} -gdirectory {} -goutfile {} -auto Y"\
    .format(algn_file,winsize,graph,self.path,title))
    self.run("(display './outputs/{}.{}' &)".format(title,graph))  


  def motifs(self,acc="",align=""):
    if self.check_file(self.list_of_acc, self.alignment_file):
      acc = self.list_of_acc
      align = self.alignment_file
    elif acc == "" or align == "":
      throw_err(self.out['motif_err'])
    self.splitter.process_motifs(acc,align)
  
  
  def filter(self,max_seq,title="filtered_alignment.fasta"):
    counter = 0
    outf = self.path + "_accessions_{}".format(max_seq) + title
    filtered = self.path + title + "filtered.fasta"
    file_to_process = self.list_of_acc
    if self.blast_file: file_to_process = self.blast_file
    with open(file_to_process,'r') as bf: 
      with open(outf,"a") as out:
        for line in bf:
          if counter >= max_seq: break
          counter += 1
          out.write(line.split()[1]+"\n")
    self.run("/localdisk/data/BPSM/Assignment2/pullseq -i {} -n {} > {}"\
      .format(self.alignment_file,outf,filtered))
    self.fasta,self.top_250 = filtered,filtered
