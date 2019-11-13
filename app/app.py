#!/usr/bin/env python3

#import user_input, retrieve, and plot classes and abstract them
#this class is the main interface for handler.py to control the flow
#of the application.
from app.user_input import User_input
from app.retrieve import Retrieve
from app.tools import Tools
from app.spinner import Spinner
from app.ld_json import Ld_json

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
    self.summary = None
    self.fasta_file = None
  

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
  

  def align(self):
    with Spinner("Aligning sequences "): self.tools.align(self.fasta_file,\
                title="{}_{}_alignment.fasta".format(self.taxon_query,self.protein_query))


  def plot(self,max_acc=25):  
    self.write()
    #self.tools.filter(max_acc,title="{}_{}".format(self.taxon_query,self.protein_query))
    with Spinner("Building consensus sequence "): self.tools.cons(title="{}_{}_cons.fasta"\
                 .format(self.taxon_query,self.protein_query))
    with Spinner("Running BLASTP "): self.tools.blast(db_file="{}_{}_db"\
                 .format(self.taxon_query,self.protein_query),b_file="{}_{}_blast.out"\
                 .format(self.taxon_query,self.protein_query))
    self.tools.filter(max_acc,title="{}_{}".format(self.taxon_query,self.protein_query))
    self.tools.plot(title="{}_{}_graph"\
                   .format(self.taxon_query,self.protein_query))
  

  def generate_motifs(self):
    with Spinner("Writing accessions "): self.write()
    with Spinner("Generating motif files "): self.tools.motifs()


  def write(self,alt=""):
    if self.dataset:
      self.tools.write(self.dataset,self.protein_query,self.taxon_query)
    else:
      print(self.out['missing_fasta'])


  def build_dataset(self,typ="all"):
  #  gets list of all taxa produced from search
    self.dataset = self.ncbi_api.taxa_protein_dict(self.get_fasta(),typ)
    return self.dataset  


  def get_summary(self):
    self.summary = self.ncbi_api.summary(self.protein_query,self.taxon_query)
    return self.summary


  #TODO refactor to be property
  def get_fasta(self):
    #initiates ncbi search using esearch and efetch
    self.fasta,self.fasta_file = self.ncbi_api.retrieve(self.protein_query,self.taxon_query)  
    return self.fasta
