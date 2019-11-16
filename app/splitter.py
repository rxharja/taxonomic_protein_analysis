#!/usr/bin/env python3
import subprocess,os

#this class handles all of the splitting of the fasta files, calling skipredundant, and also processing the motifs. I couldn't really think of a better name.
class Splitter:

  #We initialize our paths to store our files and threshold value, then we create our directories if we have not made them yet
  def __init__(self):
    self.threshold_val = 100
    self.path_motif = "./outputs/motifs/"
    self.path_species = "./outputs/species/"
    #self.db_run = False
    if not os.path.isdir(self.path_motif): os.mkdir(self.path_motif)
    if not os.path.isdir(self.path_species): os.mkdir(self.path_species)

  #skip redundant is called twice, one for the accessions we keep and one for the ones we don't. we use the file with the ones we dont keep later when we update our dataset in the app class
  def skip(self,acc,title):
    #Print to screen and then pipe it to a file so they all fit into one file
    subprocess.call('skipredundant -sequences {} -threshold {} -outseq stdout -auto Y >> {}'.format(acc,self.threshold_val,title),shell=True)
    subprocess.call('skipredundant -sequences {} -threshold {} -redundantoutseq stdout -auto Y -warning N >> {}'.format(acc,self.threshold_val,"to_pop"),shell=True)

  #this calls pullseq which takes a fasta and a file containing accessions, then outputs the fastas with .fasta appended to the file name
  def pull(self,fasta,acc):
    subprocess.call("/localdisk/data/BPSM/Assignment2/pullseq -i {} -n {} > {}".format(fasta,acc,acc+'.fasta'),shell=True)     

  #given our dataset in dict format, a fasta file, and a title, we loop through our species in our dict, handle the names of our title here to make sure theyre standardized, then write each accession associated with that species to an individual file. We then pull those sequences into their own fasta file and run skipredundant on them to generate only 2 files, to_pop (we discard these) and the file we keep.
  def process_redundant(self,fasta,dic,title):
    for species in dic.keys():
      fpath = self.path_species+species.replace(" ","_")
      fpath_fasta = self.path_species+species.replace(" ","_")+'.fasta'
      with open(fpath,'w') as f:
        for acc in dic[species]:
          print(acc,file=f)
      self.pull(fasta,fpath)
      self.skip(fpath_fasta,title)
    #skip redundant likes making files of the ones you keep even though you're doing redundantoutseq, so we remove them with a subprocess.call to rm
    subprocess.call('rm -rf *.keep',shell=True)
    #we return the actual data for the fasta and the title of the fasta as we will update our fasta to the one with no redundancies, so this goes from splitter > tools > app 
    return open(title,"r").read(),title

  #this method takes a list of accessions, in our case the total list of accessions, a fasta file to which they belong, and then splits them into individual fastas, one per accession. This needs to be done for patmatmotifs to work properly as we  can only process one at a time.
  def split_fasta(self,accs,fasta,by="single"):
    with open(accs,"r") as f:
      for line in f:
        line = line.replace("\n","")
        loc = self.path_motif + line
        #make new file containing just 1 accession based on line we are processing in accession fasta
        with open(loc,'w') as acc_f:
          acc_f.write(line)
        #pull the fastas for each one
        self.pull(fasta,loc)

  #we call the method defined above to generate our individual fastas, then we use the same accessions we passed into that variables to loop through our generated files and compile all the accessions that have a hitcount of greater than 0 to our output file 
  def process_motifs(self,fasta,accs,title):
    self.split_fasta(accs,fasta)
    with open(accs,"r") as f:
      for line in f:
        line = self.path_motif + line.replace("\n","") + ".fasta"
        try:
          motif = subprocess.check_output("patmatmotifs {} stdout -auto Y| grep 'HitCount' ".format(line),shell=True).decode('utf-8')
          if int(motif.split()[-1])!=0:
            subprocess.call("patmatmotifs {} stdout -auto Y >> {}".format(line,self.path_motif+title),shell=True)
        except:
          print("Can't process {}, non-standard accession!".format(line))
    return self.path_motif + title

  #used in the advanced menu to set the threshold for skipredundancy. Same handling in all other cases of advanced menu assigning
  def set_threshold(self):
    val = input("3. Redundancy Match Threshold(0-100): ")
    try:
      if int(val) >= 0 and int(val) <= 100: self.threshold_val = int(val)
      else: print("Your value must be between 0 and 100")
    except: print("Your value must be an integer")
