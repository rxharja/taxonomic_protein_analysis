#!/usr/bin/env python3
from app.app import App
from handler.handler import Handler
from app.spinner import Spinner

def handle(obj,handler):
  #Here, the user will be able to change any taxon or protein input they may have entered that they're not happy with. if they are happy with it, a check on the quality of the taxon choice is done, and the user will be walked through potential new taxons based on the input taxon if the taxon input was too vague. If the user is happy with their choices, they move onto the next step.
  handler.input_logic(obj)
  #The 'with  spinner' block just displays a spinning wheel so the user knows the program is running, because some processes take a long time. Here, a count summary is downloaded from esummary and shown to the user. There are checks in place that will not let the user proceed if the summary yields no results. 
  with Spinner("Generating summary "): obj.get_summary()
  #The user is asked is they wish to proceed based on the results they see, if not, the user is taken back to the query input.
  if not handler.proceed(obj.summary): return handle(obj,handler)
  #Using the spinner again because there is waiting involved in this step. The dataset is built from a efetch of the GB based on the query, and then the fasta is pulled the same way
  with Spinner("Downloading data "): 
    obj.build_dataset()
    obj.get_fasta()
  #The results of the number of accessions and total species as well as the top 5 species in terms of accession count are displayed to the user so they can make choice of whether they'd like to continue or not.
  if not handler.count_results(obj.total_seqs(),obj.total_species(),obj): return handle(obj,handler)
  #If the user chose to remove redundant sequences, this is run here. 
  if handler.path_list[0]:
    #This splits the fasta file into sequences per species, and runs skip redundant on each file so only redundant sequences within species are removed.
    obj.process_redundant()
    #The dataset is updated and displayed to the user. They are asked once again if they wish to proceed with their new data, if not, they are taken back to the input screen.
    if not handler.count_results(obj.total_seqs(),obj.total_species(),obj): return handle(obj,handler)
  #the clustalo alignment is run on the dataset and an alignment file is returned. That alignment file is then used to build a consensus sequence. A blast database is built from the dataset, and the consensus sequence is matched against that dataset to produce a list of the top 250(or user defined) most identical accessions. The program always outputs this if everything in Handler.welcome() isnt checked
  obj.align()
  #if the user chose to run the plot, the plot is built from the top 250 accessions of the dataset using plotcon, displayed to the screen, and saved as an svg
  if handler.path_list[1]:obj.plot()
  #If motifs were chosen, patmatmotifs is run against the top 250 accessions, which are all split into individual files containing 1 accession. pullseq is run to pull the alignment fasta for each accession, then it is all compiled into one file and displayed to the screen.
  if handler.path_list[2]:print(obj.generate_motifs())
  #if tree is chosen, the tree is built from the top 250 accessions in the dataset using the alignment file and iqtree. This process takes forever, so the user is told that it may take a while.
  if handler.path_list[3]: obj.tree()
  #once the program is finished running, the locations of all the files that were generated are printed to the screen so the user knows where to retrieve them.
  obj.file_locs()

def run_app():
  #initialize our app class with empty values for taxon and protein as we will set these after we decide what the user wishes to run and what advanced settings will be changed before setting taxon and protein query. The classes need to beinitialized in order to save any changes to the state
  app = App("","")
  #here, the welcome information is printed, a list of what the user may want to run is displayed and features can be turned on or off, or advanced settings like bootstrapping, esearch retmax, max accessions processed can all be tweaked. Handler.path_list booleans are turned on or off here which will be used to navigate the program's steps in handle()
  handler = Handler.welcome(app)
  #have the user assign their taxon and protein choices, user input for this is handled in the user_input class
  app.taxon_query = "taxonomy"
  app.protein_query = "protein"
  #run the function above with our basal set parameters
  handle(app,handler)

run_app()
