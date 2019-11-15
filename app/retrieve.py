#!usr/bin/env python3
import subprocess,re
#retrieve class uses subprocess to call esearch and efetch to generate a fasta file given a protein and taxon.
#The fasta file is processed into a dictionary of accessions/protein sequences per species

class Retrieve():
  def __init__(self):
    self.fasta = None


  @staticmethod  
  def search_str(taxon,*argv):
    if re.match("\d+",taxon):
      #TODO: figure out order of numbers and txid
      taxon = taxon + args[0]  
    if len(argv) < 3:
      return  "esearch -db {} -retmax '10000' -query '{}'".format(argv[1],taxon)
    return "esearch -db {} -retmax 10000 -query '{}[Organism:exp] AND {} NOT PARTIAL'"\
      .format(argv[1],taxon,argv[2])

  @staticmethod
  def fetch_str(db,form):
    return  " | efetch -db {} -format {} ".format(db,form)
  
  @staticmethod
  def summary_str(form):
    return " | esummary -format {} ".format(form)

  @staticmethod
  def run(process,c=True):
    if c:
      return subprocess.check_output(process,shell=True)
    return subprocess.call(process,shell=True)


  def get_taxa(self, taxon, db="Taxonomy"):
    tax = self.run(self.search_str(taxon,"UID",db) + self.fetch_str(db,"txt"))
    tax = tax.decode("utf-8").replace("    ",": ").replace("\n","")
    tax = re.split(r"\d\. ",tax)
    tax = list(filter(None,tax))
    return tax


  def summary(self, protein,taxon,db="Protein"):
    outp = self.run(self.search_str(taxon,"txid",db,protein))
    outp = outp.decode("utf-8")
    return re.findall(r"<Count>.*</Count>",outp)[0].replace("<Count>","").replace("</Count>","")


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
