#!/usr/bin/env python3
import subprocess,os

class Splitter:

  def __init__(self):
    self.path = "./outputs/motifs/"
    if not os.path.isdir(self.path): os.mkdir(self.path)


  def split_fasta(self,accs,fasta):
   with open(accs,"r") as f:
      for line in f:
        line = line.replace("\n","")
        loc = self.path + line
        with open(loc,'w') as acc_f:
          acc_f.write(line)
        subprocess.call("/localdisk/data/BPSM/Assignment2/pullseq -i {} -n {} > {}"\
                       .format(fasta,loc,loc+'.fasta'),shell=True)


  def process_motifs(self,fasta,accs):
    self.split_fasta(accs,fasta)
    with open(accs,"r") as f:
      for line in f:
        line = self.path + line.replace("\n","") + ".fasta"
        try:
          motif = subprocess.check_output("patmatmotifs {} stdout -auto Y| grep 'HitCount' "\
                                          .format(line),shell=True).decode('utf-8')
          if int(motif.split()[-1])!=0:
            subprocess.call("patmatmotifs {} stdout -auto Y >> {}"\
                            .format(line,self.path+"motifs.out"),shell=True)
        except:
          print("Can't process {}, non-standard accession!".format(line))
