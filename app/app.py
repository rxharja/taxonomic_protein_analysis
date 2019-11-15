#/usr/bin/env python3

#import user_input, retrieve, and plot classes and abstract them
#this class is the main interface for handler.py to control the flow
#of the application.
from app.user_input import User_input
from app.retrieve import Retrieve
from app.tools import Tools
from app.spinner import Spinner
from app.ld_json import Ld_json
import re,os

class App:
  #Initializer / instance attributes
  def __init__(self, taxonomy, protein):
    self.out = Ld_json().app
    self.Taxonomy = taxonomy
    self.Protein = protein
    self.ncbi_api = Retrieve()
    self.tools = Tools()
    self.dataset = None
    self.fasta = None
    self.gb = None
    self.summary = None
    self.fasta_file = None
    self.motifs = None
 

  @classmethod
  def from_class(cls):
    return cls(User_input.from_input("taxonomy"),
         User_input.from_input("protein")
    )

  @property
  def taxon_query(self):
    return self.Taxonomy.val


  @taxon_query.setter
  def taxon_query(self,inp):
    if inp != "taxonomy":
      self.Taxonomy = User_input.from_param(inp,"taxonomy")
    else:
      self.Taxonomy = User_input.from_input("taxonomy")


  @property
  def protein_query(self):
    return self.Protein.val


  @protein_query.setter
  def protein_query(self,inp):
    self.Protein = User_input.from_input("protein")
 
  
  def total_species(self):
    return len(self.dataset.keys())


  def total_seqs(self):
    return sum(1 for species in self.dataset for acc in self.dataset[species])
  

  def get_taxa(self):
    #given self.taxon_query, return list of
    return self.ncbi_api.get_taxa(self.taxon_query,"Taxonomy")
  

  def align(self,max_acc=250):
    self.write()
    with Spinner("Aligning sequences "): self.tools.align(self.fasta_file,title="{}_{}_alignment.fasta".format(self.taxon_query,self.protein_query)) 
    with Spinner("Building consensus sequence "): self.tools.cons(title="{}_{}_cons.fasta".format(self.taxon_query,self.protein_query))
    with Spinner("Running BLASTP "): self.tools.blast(db_file="{}_{}_db".format(self.taxon_query,self.protein_query),b_file="{}_{}_blast.out".format(self.taxon_query,self.protein_query))
    self.tools.filter(max_acc,title="{}_{}".format(self.taxon_query,self.protein_query))


  def plot(self):  
    self.tools.plot(title="{}_{}_graph"\
                   .format(self.taxon_query,self.protein_query))
 

  def generate_motifs(self):
    if not self.tools.list_of_acc: 
      with Spinner("Writing accessions "): self.write()
    with Spinner("Generating motif files "): 
      self.motifs = self.tools.motifs("{}_{}_motifs.out".format(self.taxon_query,self.protein_query)) 
    return self.motifs 
     
  def write(self,alt=""):
    if self.dataset:
      self.tools.write(self.dataset,self.protein_query,self.taxon_query)
    else:
      print(self.out['missing_fasta'])


  def build_dataset(self):
  #  gets list of all taxa produced from search
    if not self.gb: self.dataset = self.ncbi_api.dict_from_gb(self.get_gb())
    else: self.dataset = self.ncbi_api.dict_from_gb(self.gb)
    return self.dataset  


  def update_dataset(self):
    new_data = open('to_pop','r').read()
    to_pop = re.findall(r"[A-Z]+_?\d+\.\d",new_data)
    for org in self.dataset.keys():
      self.dataset[org] = [x for x in self.dataset[org] if x not in to_pop]
    os.remove('to_pop') 

  def get_summary(self):
    self.summary = self.ncbi_api.summary(self.protein_query,self.taxon_query)
    return self.summary


  def get_fasta(self):
    #initiates ncbi search using esearch and efetch
    self.fasta,self.fasta_file = self.ncbi_api.retrieve(self.protein_query,self.taxon_query)  
    return self.fasta


  def get_gb(self):
    self.gb = self.ncbi_api.retrieve(self.protein_query,self.taxon_query,form="gb")
    return self.gb


  def process_redundant(self,dataset=None):
    if self.dataset: 
      dataset = self.dataset
    elif not dataset:
      print(self.out['missing_dataset'])
    with Spinner("Yeeting redundant data "):
      self.fasta,self.fasta_file = self.tools.filter_redundant(self.fasta_file,self.dataset,"{}_{}".format(self.taxon_query,self.protein_query)) 
    self.update_dataset()


  def tree(self):
    with Spinner('Building tree, this may take a while '): self.tools.tree()

  
  def file_locs(self):
    print(self.out["locations"])
    if self.fasta_file: print(self.out['fasta'].format(self.fasta_file))
    if self.tools.alignment_file: print(self.out["alignment"].format(self.tools.alignment_file))
    if self.tools.plot_file: print(self.out['graph'].format(self.tools.plot_file))
    if self.tools.motifs_file: print(self.out['motifs'].format(self.tools.motifs_file))
    if self.tools.tree_file: print(self.out['tree'].format(self.tools.tree_file))
