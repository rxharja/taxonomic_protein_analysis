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

#This is our main class which we pass all of our other classes into. This is where our blueprint for our program is at its most abstract.
class App:
  #Initialize all of our other classes from here and assign them to our class. Also initiliaze some empty variables which will be assigned later as our program progresses and generates some files and data.
  def __init__(self, taxonomy, protein):
    self.out = Ld_json().app
    self.Taxonomy = taxonomy
    self.Protein = protein
    self.ncbi_api = Retrieve()
    self.tools = Tools()
    self.max_acc = 250
    self.dataset = None
    self.fasta = None
    self.gb = None
    self.summary = None
    self.fasta_file = None
    self.motifs = None
 

  #this method is currently not used, I was using it to initialize the App class with taxon and protein query first, but now I set them to empty so I can show the user the advanced screen before they make any query inputs, then just assign them with the property assigners declared below. Another developer can do something with this if they so choose though 
  @classmethod
  def from_class(cls):
    return cls(User_input.from_input("taxonomy"),
         User_input.from_input("protein")
    )

  #returns our taxon query
  @property
  def taxon_query(self):
    return self.Taxonomy.user_input

  #this gets called in the advanced menu and controls what a user can input for the max number of accessions to process
  def set_max_acc(self):
    #if the value is within 0 to 250, accept it and reassign max_acc, otherwise don't do anything and tell the user the appropriate thing to enter
    val = input("1. Maximum Accessions to Download(0-250): ")
    try: 
      if int(val) <= 250 and int(val) >= 2: self.max_acc = int(val)
      else: print("Your value must be a number between 2 and 250")
    except: print("Your value must be an integer")

  #if this function is called with taxonomy as a param, it will give the user a message to enter a taxon, otherwise itll just do a direct assignment of whatever the input you passed was, which is not equal to taxonomy
  @taxon_query.setter
  def taxon_query(self,inp):
    if inp != "taxonomy":
      self.Taxonomy = User_input.from_param(inp,"taxonomy")
    else:
      self.Taxonomy = User_input.from_input("taxonomy")

  #getter for protein_query
  @property
  def protein_query(self):
    return self.Protein.user_input

  #setter for protein query, for some reason I didn't give the same branching for taxon setting, probably because setting the taxon is more restricted and sophisticated than setting the protein.
  @protein_query.setter
  def protein_query(self,inp):
    self.Protein = User_input.from_input("protein")
 
  #get the total number of species from the dataset which is passed into handler to show the user. If dataset isnt there yet, it throws a print statement.
  def total_species(self):
    try: return len(self.dataset.keys())
    except: print("you must download the data first using build_dataset")

  #returns the total number of accessions using sum, it loops through the list associated with the key and counts them all.
  def total_seqs(self):
    return sum(1 for species in self.dataset for acc in self.dataset[species])
  
  #this talks to the retrieve/ncbi_api class to get a list of the taxa associated with the taxon_query. this gets passed to handler to check to see if it can be narrowed down to a more specific choice or not.
  def get_taxa(self):
    return self.ncbi_api.get_taxa(self.taxon_query,"Taxonomy")
  
  #This runs regardless of if the user turns off everything in the beginning of the program. It always will generate an alignment, run blast, build the consensus, and then get the top 250 accessions.
  def align(self):
    #This writes the the accessions to an output file based on the dataset assigned to the app class
    self.write()
    #This takes the fasta_file location and a title as an input to produce the alignment output. The fasta_file location will have been defined once the user has downloaded the appropriate data which is necessary to get to this step. Because this process takes a while, its done with a little spinning wheel coded in the Spinner class.
    with Spinner("Aligning sequences "): self.tools.align(self.fasta_file,title="{}_{}_alignment.fasta".format(self.taxon_query,self.protein_query))
    #Next we run the consensus which we do using the alignment fasta. the tools class keeps track of all the files we've been generating so its all handled there 
    with Spinner("Building consensus sequence "): self.tools.cons(title="{}_{}_cons.fasta".format(self.taxon_query,self.protein_query))
    #Then using the consensus and alignment, we build a database with the alignment file, then run the consensus against it to get the list of top 250 accessions
    with Spinner("Running BLASTP "): self.tools.blast(db_file="{}_{}_db".format(self.taxon_query,self.protein_query),b_file="{}_{}_blast.out".format(self.taxon_query,self.protein_query))
    #this will filter the alignment fasta based on the list of however many taxons we set as our max with write() and rename it to something_filitered_alignment. 
    self.tools.filter(self.max_acc,title="{}_{}".format(self.taxon_query,self.protein_query))

  #calls plotcon and saves the output to an svg, displays it to the screen using display
  def plot(self):  
    self.tools.plot(title="{}_{}_graph".format(self.taxon_query,self.protein_query))
 
  #generates motifs by splitting our top accessions into individuals files and then running patmatmotifs on each one
  def generate_motifs(self):
    #if there isnt a list of accessions yet, write() is called to make one
    if not self.tools.list_of_acc: 
      with Spinner("Writing accessions "): self.write()
    #generates motif files and assigns the output to self.motifs
    with Spinner("Generating motif files "): self.motifs = self.tools.motifs("{}_{}_motifs.out".format(self.taxon_query,self.protein_query)) 
    return self.motifs 
    
  #if dataset is built, we write the accessions in there to a file to be processed with other functions that need them in a file later on  
  def write(self,alt=""):
    if self.dataset:
      self.tools.write(self.dataset,self.protein_query,self.taxon_query)
    else:
      print(self.out['missing_fasta'])

  #if the gb file is not built yet, then we pass get_gb() into the dict_from_gb file, this retrieves the gb file from ncbi and extracts the appropriate data into a dict. It can also run normally if gb is assigned.
  def build_dataset(self):
    if not self.gb: self.dataset = self.ncbi_api.dict_from_gb(self.get_gb())
    else: self.dataset = self.ncbi_api.dict_from_gb(self.gb)
    return self.dataset  

  #this is run only when we filter for redundancies and have to update our dataset. skipredundant puts out a redundant list which we named to_pop, from there we extract the accessions and then only keep the accessions which are not on the to_pop list
  def update_dataset(self):
    new_data = open('to_pop','r').read()
    to_pop = re.findall(r"[A-Z]+_?\d+\.\d",new_data)
    for org in self.dataset.keys():
      self.dataset[org] = [x for x in self.dataset[org] if x not in to_pop]
    os.remove('to_pop') 

  #contacts the ncbi database and downloads a count of accessions using summary and taking our two queries.
  def get_summary(self):
    self.summary = self.ncbi_api.summary(self.protein_query,self.taxon_query)
    return self.summary

  #pulls the fasta file from ncbi database using esearch and efetch
  def get_fasta(self):
    self.fasta,self.fasta_file = self.ncbi_api.retrieve(self.protein_query,self.taxon_query)  
    return self.fasta

  #does the same thing but but changes format to genbank instead of fasta
  def get_gb(self):
    self.gb = self.ncbi_api.retrieve(self.protein_query,self.taxon_query,form="gb")
    return self.gb

  #uses skipredundant to process identical sequences within a given taxon, default is set to 100% threshold but a user can change this in the advanced settings
  def process_redundant(self,dataset=None):
    #gives the option to pass your own dataset in or use the one built by the program
    if self.dataset: 
      dataset = self.dataset
    elif not dataset:
      print(self.out['missing_dataset'])
    #input is our fasta file to process, at this stage it is just a fasta as we dont want to do this after the alignment since it would make the alignment process longer. It returns the fasta as a variable which can be retrieved with self.fasta and the location of the file 
    with Spinner("Removing exact sequences within taxa "):
      self.fasta,self.fasta_file = self.tools.filter_redundant(self.fasta_file,self.dataset,"{}_{}".format(self.taxon_query,self.protein_query)) 
    self.update_dataset()

  #calls iqtree and processes the alignment file generated, the error is handled in tools if no alignment file supplied
  def tree(self):
    with Spinner('Building tree, this may take a while '): self.tools.tree()

  #just prints out the locations for each of the files if the file exists, meaning if this part of the code was run, this will print 
  def file_locs(self):
    print(self.out["locations"])
    if self.fasta_file: print(self.out['fasta'].format(self.fasta_file))
    if self.tools.alignment_file: print(self.out["alignment"].format(self.tools.alignment_file))
    if self.tools.plot_file: print(self.out['graph'].format(self.tools.plot_file))
    if self.tools.motifs_file: print(self.out['motifs'].format(self.tools.motifs_file))
    if self.tools.tree_file: print(self.out['tree'].format(self.tools.tree_file))
