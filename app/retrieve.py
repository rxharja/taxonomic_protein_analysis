#!usr/bin/env python3
import subprocess,re
#retrieve class uses subprocess to call esearch and efetch to generate a fasta file given a protein and taxon.
#The fasta file is processed into a dictionary of accessions/protein sequences per species

class Retrieve():

  #stores the fasta output and the retmax value
  def __init__(self):
    self.fasta = None
    self.retmax = 10000


  #takes a taxon name and up to 3 additional arguments, but potentially 2. If its 2 then its used to get the taxa info only, if its 3 then its combined with efetch for gb and fasta pulling
  @staticmethod  
  def search_str(taxon,*argv):
     #also handle append uid to the end of a taxon if its numbers only
    if re.match("\d+",taxon):
      taxon = taxon + args[0]  
    if len(argv) < 3:
      return  "esearch -db {} -query '{}'".format(argv[1],taxon)
    return "esearch -db {} -query '{}[Organism:exp] AND {} NOT PARTIAL'".format(argv[1],taxon,argv[2])


  #returns the efetch string which gets combined with esearch, can pass in format and db 
  @staticmethod
  def fetch_str(db,form):
    return  " | efetch -db {} -format {} ".format(db,form)
  
  #summary string used to get accession counts to display summary to user, can request other formats, not actually used in this script but another dev might find it useful
  @staticmethod
  def summary_str(form):
    return " | esummary -format {} ".format(form)

  #just abstracts the subprocess call/check_output, pass in a bool for c to get check_output or call
  @staticmethod
  def run(process,c=True):
    if c:
      return subprocess.check_output(process,shell=True)
    return subprocess.call(process,shell=True)

  #redefine retmax in the advanced menu, handle user input by checking if integer or not within the specified range. 2 is the minimum because we need at least 2 for the program to work
  def set_retmax(self):
    val = input("1. Maximum Accessions to Download(2-10000): ")
    try:
      if int(val) >= 2 and int(val) <= 10000: self.retmax = int(val)
      else: print("Your value must be a number between 2 and 10000")
    except: print("Your value must be an integer")


  #this pulls the taxa which we will pass into the handler for the user to choose a potential new one. We assign the output of the efetch to tax and decode it to utf-8, then modify it so it can fit nicely into one element and to output to user, then we split by the numbers because we will assign our own numbers later, and then filter out the empty elements 
  def get_taxa(self, taxon, db="Taxonomy"):
    tax = self.run(self.search_str(taxon,"UID",db) + self.fetch_str(db,"txt"))
    tax = tax.decode("utf-8").replace("    ",": ").replace("\n","")
    tax = re.split(r"\d\. ",tax)
    tax = list(filter(None,tax))
    return tax

  #gets a summary by just calling esearch and assigning it to outp with our search parameters, then we filter the count section using a regex and returning it 
  def summary(self, protein,taxon,db="Protein"):
    outp = self.run(self.search_str(taxon,"txid",db,protein))
    outp = outp.decode("utf-8")
    return re.findall(r"<Count>.*</Count>",outp)[0].replace("<Count>","").replace("</Count>","")

  #here we make sure we replace any empty spaces for our file names, then we pull the fasta and save it as taxon_protein.fasta. We return the fasta if form=fasta of course but its also used to get the gb file, which we don't save so we first convert it from our variable to utf-8 from bytestring
  def retrieve(self,protein,taxon,db="Protein",form="fasta"):
    #returns fasta file given search parameters
    protein_f = protein.replace(" ","_")
    taxon_f = taxon.replace(" ","_")
    if form=="fasta": 
      fasta_file = "./outputs/{}_{}.fasta".format(taxon_f,protein_f)
      self.run(self.search_str(taxon,"txid",db,protein)+self.fetch_str(db,form)+"> {}".format(fasta_file),False)
      outp = open(fasta_file,"r").read()
      return outp,fasta_file
    return self.run(self.search_str(taxon,"txid",db,protein)+self.fetch_str(db,form)).decode("utf-8")

  #this method isnt actually used anymore because of a bug I encountered when searching for Mus musculus. The method takes all the information from the fasta file including Accession, species name, and protein sequence and builds a dictionary from it. You can choose Species:Acc, Species:ProteinSequence, or Species:{Acc:ProteinSeq}. One fasta result did not have the typical header format and didnt have the species name at all in the header, so that messed things up downstream a bit. Still keeping it here though because another developer might find it useful to build a dict from a fasta file 
  def dict_from_fasta(self,f,typ):
    #returns list of all taxa from fasta files
    t_p_dict = {}
    species = [itm.replace("[","").replace("]","") for itm in re.findall(r"\[{1}[A-Z]{1}[a-z]+ [a-z]*\]{1}",f)]
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
    else:
      accessions = [itm for itm in re.findall(r"[A-Z]+_?\d+\.\d",f)]
      proteins = re.split(r">.{0,150}]",f.replace("\n",""))
      proteins = list(filter(None,proteins))
      assert(len(accessions) == len(proteins))
      for i in range(len(species)):
        try:
          t_p_dict[species[i]] = {**t_p_dict[species[i]],accessions[i]:proteins[i]}
        except:
          t_p_dict = {**t_p_dict, species[i]:{accessions[i]:[proteins[i]]}}
    return t_p_dict

  #this one replaced the method above. It uses regular expressions to extract from the gb file which are very standardized and assigns them to lists using findall. We assert that the lengths of our lists are the same. Then we build our dict in our try and except area
  def dict_from_gb(self,gb):
    t_p_dict = {}
    orgs = re.findall(r'ORGANISM.*',gb)
    orgs = [org.replace("ORGANISM","").strip() for org in orgs]
    accs = re.findall(r'VERSION.*',gb)
    accs = [acc.replace("VERSION","").strip() for acc in accs]
    assert(len(orgs) == len(accs))
    for i in range(len(orgs)):
      try:
        t_p_dict[orgs[i]] += [accs[i]]
      except:
        t_p_dict[orgs[i]] = [accs[i]]
    return t_p_dict
