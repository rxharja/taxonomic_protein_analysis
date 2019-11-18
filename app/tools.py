#!/usr/bin/env python3
import subprocess,os
from app.ld_json import Ld_json
from app.splitter import Splitter

#This is our swiss army knife class. I went back and forth on structuring these methods defined in this class but decided on just putting them all into one class called tools because that would have been too many tiny files, maybe in the future I'll refactor it to be that way
class Tools:
  #import our outputs from the json file
  out = Ld_json().tools

  def __init__(self,path="./outputs/"):
    #store pathways of each file as they're generated as strings. Make output directory if it does not exist upon initialising
    if not os.path.isdir(path): os.mkdir(path)
    self.fasta = None
    self.alignment_file = None
    self.consensus = None
    self.db = None
    self.blast_file = None
    self.top_250 = None
    self.list_of_acc = None
    self.plot_file = None
    self.motifs_file = None
    self.tree_file = None
    self.path = path
    self.splitter = Splitter()
    self.bb = 1000


  @staticmethod
  def throw_err(outp):
    #some reusable code to print an error the screen and then exit the program
    print(outp)
    exit()


  @staticmethod
  def check_file(*argv):
    #takes each file passed into function as a list, evaluates if they exist and appends them to a list. If they all exist, returns true, otherwise false.
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

 
   #this takes our dataset, takes the accessions, and writes them all into a file called taxon_protein_accs.fasta 
  def write(self,inp_f,p="protein",t="taxon",alt=""):
    p = p.replace(" ","_")
    t = t.replace(" ","_")
    title = self.path
    if alt == "":
      title +="{}_{}_accs.fasta".format(t,p)
    else:
      title += alt #branch here if someone decided to include a different title
    with open(title,"w+") as f: #write all of our accessions into the file
      for species in inp_f.keys():
        for acc in inp_f[species]:
          f.write(acc+"\n")
    self.list_of_acc = title #assign our list_of_acc file to our state

  def align(self,fasta,title="alignment.fasta"):
    #calls clustalo to align the fasta file and outputs it to default alignment.fasta in outputs folder
    title = self.path + title.replace(" ","_") #handle any spaces in our title
    self.fasta = fasta #assign the fasta input here as the fasta for this class
    if self.check_file(self.fasta): #make sure the file exists
      self.run("clustalo -i {} -t protein --threads 12  --force -o {}".format(self.fasta,title))
      self.alignment_file = title #then we assign our title as our alignment_file location
    else:
      self.throw_err(self.out['alignment_err'])


  def cons(self,title="consensus.fasta"):
    #calls cons from emboss tools to create a conensus sequence of our aligned sequences, outputs as default consensus.fasta to outputs folder
    title = self.path + title.replace(" ","_") #handle spaces in title, make sure our file exists, then run cons on our alignment file. handle lack of alignment file
    if self.check_file(self.alignment_file):
      self.run("cons -sprotein1 {} -outseq {} -auto Y".format(self.alignment_file,title))
      self.consensus = title #assign location of consensus sequence to state
    else:
      self.throw_err(self.out['consensus_err'])  
  

  def blast(self,db_file="output_db",b_file="blastp.out"):
    #runs two processes, first creates a blast database given fasta file to output_db
    if self.check_file(self.consensus,self.fasta): #make sure we have the necessary files, fasta and consensus.
      db_file = self.path + db_file.replace(" ","_") #handle irregularities in title
      b_file = self.path + b_file.replace(" ","_")
      self.run("makeblastdb -in {} -dbtype prot -out {}".format(self.fasta,db_file)) #make the db
      self.db = db_file #set it to state
      self.run("blastp -db {} -query {} -max_hsps 1 -outfmt 6 > {}".format(self.db,self.consensus,b_file)) #run the blast
      self.blast_file = b_file #set the file to the state
    else:
      self.throw_err(self.out['blast_err'])

  #runs plotcon with the alignment file and some predefined variables. Will take another alignment file as an input but it defaults to the one saved to the state if none provided
  def plot(self,algn_file="",winsize='4',graph='svg',title="plotcon"):
    if not algn_file:
      if self.alignment_file:
        algn_file = self.alignment_file
      else:
        self.throw_err(self.out['plot_err'])
    title = title.replace(" ","_")
    self.run("plotcon {} -winsize {} -graph {} -gdirectory {} -goutfile {} -auto Y".format(algn_file,winsize,graph,self.path,title))
    self.run("(display './outputs/{}.{}' &)".format(title,graph)) #run the display in a subshell as to not stop the script from running 
    self.plot_file =self.path+ title + '.svg' #save pathway of plot to state

  #abstracts the splitter.process_motifs method chooses the right files to pass into it, then returns the data from the motifs to app class
  def motifs(self,title,acc="",align=""):
    title = title.replace(" ","_") 
    if self.check_file(self.list_of_acc, self.alignment_file):
      acc = self.list_of_acc
      align = self.alignment_file
    elif acc == "" or align == "":
      throw_err(self.out['motif_err'])
    self.motifs_file = self.splitter.process_motifs(align,acc,title)
    return open(self.motifs_file,'r').read()

  #this takes the maximum sequences we want, handles the title for spaces, and takes the blast file and gets the top however many accessions, then writes them to a file, then we run pullseq, which I suppose I could have called self.splitter.pull for this, but this was before I wrote that. anyway the output is our final filtered fasta
  def filter(self,max_seq,title="filtered_alignment.fasta"):
    counter = 0
    title = title.replace(" ","_")
    outf = self.path + "accessions_{}_".format(max_seq) + title
    filtered = self.path + title + "filtered.fasta"
    file_to_process = self.list_of_acc
    if self.blast_file: file_to_process = self.blast_file
    with open(file_to_process,'r') as bf: 
      with open(outf,"a") as out:
        for line in bf:
          if counter >= max_seq: break #counter limit defined by max_seq
          counter += 1
          out.write(line.split()[1]+"\n")
    self.run("/localdisk/data/BPSM/Assignment2/pullseq -i {} -n {} > {}".format(self.alignment_file,outf,filtered))
    self.alignment_file,self.list_of_acc = filtered,outf

  #this abstracts our splitter.process_redundant method and returns our new raw fasta(the fasta data) and the file name
  def filter_redundant(self,fasta,data,title): 
    raw_fasta,self.fasta = self.splitter.process_redundant(fasta,data,self.path+title.replace(" ","_")+"_no_redundant.fasta")
    return raw_fasta,self.fasta

  #advanced menu setter for babybootstrap which gets passed to self.tree. standard for all advanced menu assignments 
  def set_bb(self):
    val = input("4. Phylogenetic Tree Boostrap Value(min 1000): ")
    try:
      if int(val) >= 1000: self.bb = int(val)
      else: print("Your value must be greater than 1000")
    except: print("Your value must be an integer")
  
  #calls iq tree and prints it to the screen. Also saves file name to state
  def tree(self):
    subprocess.call('iqtree -s {} -m MFP -nt AUTO -alrt {} -bb {} -bnni'.format(self.alignment_file,self.bb,self.bb),shell=True)
    self.tree_file = self.alignment_file+'.iqtree'
    print(open(self.tree_file,'r').read())
