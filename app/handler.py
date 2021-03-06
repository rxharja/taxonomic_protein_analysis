#!/usr/bin/env python3
from app.spinner import Spinner
from app.ld_json import Ld_json

class Handler:
  #dictionary containing all statements to print to the screen for user
  out = Ld_json().handler
  

  #initialize taxon search cache
  def __init__(self,pth):
    self.taxon_cache = {}
    self.path_list = pth


  #handle user input logic: If user is happy with their taxon and protein
  #options, then move on to taxon handler. Taxon handler will check the 
  #users taxon input to see if its too vague, for example, searching for 
  #fish will generate 6 families, so a user must choose one to move on.
  #If a user does not choose one, it loops back to input_handler to change 
  #either protein or taxon again, otherwise the loop ends.
  def input_logic(self,obj):
    while True:
      if self.input_handler(obj):
        if self.taxon_handler(obj):
          break    


  #call display choices which prints a string to the screen that shows what the 
  #user inputted as queries for taxon and protein. Here the user has the option
  #to change either protein, taxon, or both. If the user is happy with their decision,
  #simply hitting enter will exit the function with True.
  def input_handler(self,obj):
    self.display_choices(obj.taxon_query,obj.protein_query)
    user_change = self.ex_check(input(self.out['user_change'])\
      .format(obj.taxon_query,obj.protein_query))
    if user_change == "1":
      obj.taxon_query = "taxonomy"
    elif user_change == "2":
      obj.protein_query = "protein"
    elif user_change == "3":
      obj.taxon_query = "taxonomy"
      obj.protein_query = "protein"
    elif user_change not in "123" and user_change != "":
      print(self.out['improper_input'])
    if user_change == "":
      return True
    return False


  #sometimes taxon queries are too vague and won't generate an appropriate data set.
  #taxon_handler checks the query against the taxonomy database to see if the query
  #was narrow enough. That basically means that if your query only produced one 
  #choice for taxon. For example birds produces only aves, but fish produces multiple.
  def taxon_handler(self,obj):
    #cache taxon choice so program doesn't call esearch | efetch every time user 
    #changes their taxon choice. So if user searches for 'aves', changes it to 'mus',
    #then decides to go back to 'aves', it won't check for different taxons.
    move_on = False
    try:
      taxons = self.taxon_cache[obj.taxon_query]  
    except:
      with Spinner("Checking taxon choice, please wait "): taxons = obj.get_taxa()
      self.taxon_cache[obj.taxon_query] = taxons
    #check to see if taxon search generated what user already searched for, if true,
    #exit taxon_handler and move on, otherwise go to choose between narrower taxa.
    if self.check_dict(self.taxon_cache,obj.taxon_query): return True
    #if the query only produced 1 hit from the taxonomy database, you're good to move on
    if len(taxons) == 1:
      move_on = True
    #if the query produced nothing from the database, print out the error message 
    if len(taxons) == 0:
      print(self.out['no_taxons'])
    else:
      while True:
        print(self.out['vague_taxons'])
        [print("{}. {}".format(i+1,taxons[i])) for i in range(len(taxons))]
        try:
          inp = input("Choice :")
          if inp in ['q','quit','exit'] or int(inp) == 0:
            break
          inp = int(inp) - 1
          choice = taxons[inp][0:taxons[inp].find(':')]
          obj.taxon_query = choice
          self.display_choices(obj.taxon_query,obj.protein_query)
          move_on = True
          break
        except:
          print(self.out['improper_choice'].format(len(taxons)))
    self.ex_check(inp)
    return move_on


  def proceed(self,results):
    if int(results) <= 1:
      print(self.out['no_results'].format(results))
      return False
    ans = self.ex_check(input(self.out['results'].format(results)))
    if ans == "":
      return True
    else:
      print("Returning")
      return False


  def count_results(self,seq,spec):
    inp = self.ex_check(input(self.out['continue_results'].format(seq,spec)))
    if inp=="": return True
    else: 
      print("Returning")
      return False

    
  @staticmethod
  def ex_check(inp):
    exits = ['exit','quit','q']
    if inp in exits:
      exit()
    return inp


  @staticmethod  
  def check_dict(d,genus):
    l = d[genus]
    for itm in l:
      if itm.lower()[0:itm.find(":")] == genus:
        return True  


  def display_choices(self,tax,prot):
    #output located in json file, takes taxonomy and protein as inputs
    #displays user's chosen queries on screen.
    return print(self.out['display'].format(tax,prot))


  @classmethod
  def welcome(cls):
    #TODO rename wildcard
    path_list = [True,True,True]
    while True:    
      path_vals = ['X' if itm  else ' ' for itm in path_list]
      print(cls.out['welcome'].format(path_vals[0],path_vals[1],path_vals[2]))
      inp = input("Value: ")
      if inp == "" or inp in ['quit','exit','q']: break
      try:
        if int(inp)==4: path_list = [True,True,True]
        elif int(inp)==5: path_list = [False,False,False]
        else: path_list[int(inp)-1] = not path_list[int(inp)-1] 
      except:
        print("Your input must be a valid integer")
    cls.ex_check(inp)
    return cls(path_list)
