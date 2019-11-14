#!/usr/bin/env python3
import subprocess,os

class Splitter:

  def __init__(self):
    self.threshold_val = 100
    self.path_motif = "./outputs/motifs/"
    self.path_species = "./outputs/species/"
    #self.db_run = False
    if not os.path.isdir(self.path_motif): os.mkdir(self.path_motif)
    if not os.path.isdir(self.path_species): os.mkdir(self.path_species)

  def skip(self,acc,title):
    subprocess.call('skipredundant -sequences {} -threshold {} -outseq stdout -auto Y >> {}'\
                    .format(acc,self.threshold_val,title),shell=True)


  def pull(self,fasta,acc):
    subprocess.call("/localdisk/data/BPSM/Assignment2/pullseq -i {} -n {} > {}"\
                       .format(fasta,acc,acc+'.fasta'),shell=True)     


  def process_redundant(self,fasta,dic,title):
    for species in dic.keys():
      fpath = self.path_species+species.replace(" ","_")
      fpath_fasta = self.path_species+species.replace(" ","_")+'.fasta'
      with open(fpath,'w') as f:
        for acc in dic[species].keys():
          print(acc,file=f)
      self.pull(fasta,fpath)
      self.skip(fpath_fasta,title)
    return open(title,"r").read(),title


  def split_fasta(self,accs,fasta,by="single"):
    with open(accs,"r") as f:
      for line in f:
        line = line.replace("\n","")
        loc = self.path_motif + line
        with open(loc,'w') as acc_f:
          acc_f.write(line)
        self.pull(fasta,loc)


  def process_motifs(self,fasta,accs,title):
    self.split_fasta(accs,fasta)
    with open(accs,"r") as f:
      for line in f:
        line = self.path_motif + line.replace("\n","") + ".fasta"
        try:
          motif = subprocess.check_output("patmatmotifs {} stdout -auto Y| grep 'HitCount' "\
                                          .format(line),shell=True).decode('utf-8')
          if int(motif.split()[-1])!=0:
            subprocess.call("patmatmotifs {} stdout -auto Y >> {}"\
                            .format(line,self.path_motif+title),shell=True)
        except:
          print("Can't process {}, non-standard accession!".format(line))
    return self.path_motif + title

  @property
  def threshold(self):
    return self.threshold


  @threshold.setter
  def threshold(self,new_threshold):
    try:
      self.threshold_val = int(new_threshold)
    except:
      print("Must be a number value")
