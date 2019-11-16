#!/usr/bin/env python3
from app.spinner import Spinner
from app.ld_json import Ld_json

#This class handles the flow of our program based on user input and whatever output the program returns.
class Handler:
  #dictionary containing all statements to print to the screen for user, all of which are stored in a json file which ar then converted into a dictionary from the Ld_json class.
  out = Ld_json().handler
  

  #initialize taxon search cache (self.taxon_cache), a list of booleans which determine which parts of the program to run (self.path_list), and a boolean that checks whether the results of the data being pulled have already been displayed, if they have it branches to show user a specific message if they filtered their data.
  def __init__(self,pth):
    self.taxon_cache = {}
    self.path_list = pth
    self.displayed_results = False


   #handle user input logic: If user is happy with their taxon and protein options, then move on to taxon handler. Taxon handler will check the users taxon input to see if its too vague, for example, searching for fish will generate 6 families, so a user must choose one to move on. If a user does not choose one, it loops back to input_handler to change either protein or taxon again, otherwise the loop ends.
  def input_logic(self,obj):
    while True:
      if self.input_handler(obj):
        if self.taxon_handler(obj):
          break    


  #call display choices which prints a string to the screen that shows what the user inputted as queries for taxon and protein. Here the user has the option to change either protein, taxon, or both. If the user is happy with their decision, simply hitting enter will exit the function with True, which will move input_logic to taxon_handler.
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


  #sometimes taxon queries are too vague and won't generate an appropriate data set. Taxon_handler checks the query against the taxonomy database to see if the query was narrow enough. That basically means that if your query only produced one choice for taxon. For example birds produces only aves, but fish produces multiple.
  def taxon_handler(self,obj):
    #cache taxon choice so program doesn't call esearch | efetch every time user changes their taxon choice. So if user searches for 'aves', changes it to 'mus', then decides to go back to 'aves', it won't check for different taxons. move_on is the boolean that decides if we exit input_logic()
    move_on = False
    try:
      #try retrieving the cached search first, didnt use the dict.get() way because I wanted to display a spinner if we had to download a new list of taxons
      taxons = self.taxon_cache[obj.taxon_query]  
    except:
      #download a list of taxons based on the query, then assign it to our search query in our dictionary cache, so next time its searched we won't have to talk to ncbi.
      with Spinner("Checking taxon choice, please wait "): taxons = obj.get_taxa()
      self.taxon_cache[obj.taxon_query] = taxons
    #sometimes if you search aves in ncbi, you get aves back, in order to stop it from keep downloading aves, we do a check to see if aves is already assigned to the list assigned to the query aves, we just exit with true
    if self.check_dict(self.taxon_cache,obj.taxon_query): return True
    #if the query only produced 1 hit from the taxonomy database, you're good to move on
    if len(taxons) == 1:
      move_on = True
    #if the query produced nothing from the database, tell the user that their search produced nothing, at this point we return false and loop to choose a new taxon. Then we'll be back here with that new taxon! 
    elif len(taxons) == 0:
      print(self.out['no_taxons'])
    else:
      while True:
        #notify user that their taxon choice needs to be refined a bit, then show them their available options
        print(self.out['vague_taxons'])
        [print("{}. {}".format(i+1,taxons[i])) for i in range(len(taxons))]
        try:
          #just in case user tries to quit the program check for that first. We'll need to exit our loop first otherwise we'll just loop forever. We have a defined function down below which checks if the user wanted to exit the program, but I can't check that in a loop, so we check it more downstream. entering 0 will just knock you back to changing a query choice.
          inp = input("Choice :")
          if inp in ['q','quit','exit'] or int(inp) == 0:
            break
          #Now we try to convert whatever their input was into a number, if its not we throw up a message telling them that wasn't right and to try again. Then we adjust their human indexing for python indexing by subtracting 1
          inp = int(inp) - 1
          #assign their choice by pointing it out in the list and getting everything up to the colon, then pass that as the new taxon query
          choice = taxons[inp][0:taxons[inp].find(':')]
          obj.taxon_query = choice
          #here we display our choices again to the user so they know what their choices were before we move on to giving them a summary, which we will, since we set move_on to true which will break us out of the input_logic loop.
          self.display_choices(obj.taxon_query,obj.protein_query)
          move_on = True
          break
        except:
          #a message telling the user their choice wasn't right, and then they'll get a chance to try again.
          print(self.out['improper_choice'].format(len(taxons)))
    #here, outside of the while loop, we check to see if we can leave the script based on the user's input. If we dont leave we just keep going by returning our boolean, if it wasnt true we'll loop back around.
      self.ex_check(inp)
    return move_on

  #this is the part that takes the summary results from esummary (which is just a count of the potential accessions we can run) and displays it to the user in a human way. It returns a boolean based on: if results were less than 1, then its an automatic false, in the runme file, it loops user back to the top of the function. If the user just hits enter, we keep going with the program, any other input it returns false and we're back to choosing our query.
  def proceed(self,results):
    if int(results) <= 1:
      #defined error message for case where we don't have enough accessions to run the program
      print(self.out['no_results'].format(results))
      return False
    #get the input from the user based on if they like their summary results or not
    ans = self.ex_check(input(self.out['results'].format(results)))
    if ans == "":
      return True
    else:
      print("Returning")
      return False

  #here we display more detailed results once we've downloaded the gb, made our dictionary, and downloaded the fasta. We show the user how many sequences and species the result has produced. We also define a case for if we've run the redundancy, which means we show the same detailed results again, but we need a different message to give to the user to show them that the result is different because we ran the redundancy.
  def count_results(self,seq,spec):
    outp = self.out['continue_results'].format(seq,spec)
    #we init this variable as false so the first time it runs its false, but after that, we set it to true so the next time it runs it shows the user results for the redundancy.
    if self.displayed_results: outp = self.out['results_redundancy'].format(seq,spec)
    inp = self.ex_check(input(outp))
    self.displayed_results = True
    if inp=="": return True
    else: 
      print("Returning")
      return False

  #wraps a user input, takes a string as an input, and checks to see if that string exists in our exit list. If it does we just leave the program, if it doesnt then we just return whatever we passed in.
  @staticmethod
  def ex_check(inp):
    exits = ['exit','quit','q']
    if inp in exits: exit()
    return inp

  #this is the method we used above in our taxon checking. we loop through through the taxa in the list associated with our taxon query. If the thing we searched for already exists in our list associated with our taxon query, then we return true and leave the loop.
  @staticmethod  
  def check_dict(d,genus):
    for itm in d[genus]:
      #make sure to only check if everything up to the colon matches since we get rid of everything after and including.
      if itm.lower()[0:itm.find(":")] == genus:
        return True  

  #just a function that prints to the screen what choices the user made for taxon and protein
  def display_choices(self,tax,prot):
    return print(self.out['display'].format(tax,prot))


  #This menu is accessed exclusively at the beginning of the program during the welcome screen. It allows the user to tweak certain parameters in some of the emboss tools, iqtree, entrez, or define our cap of samples to analyze.
  @staticmethod
  def advanced_menu(obj):
    #keep it in a while true loop as to not throw user out of menu if user input was wrong. 
    while True:
      print(Handler.out['advanced_menu'].format(obj.ncbi_api.retmax,obj.max_acc,obj.tools.splitter.threshold_val,obj.tools.bb))
      val=input(Handler.out["advanced_inp"]) 
      #this menu can only be exited if we type exit, we cannot leave the program the usual way in here so we don't check for exit statements.
      if val == "exit": break
      #here we check to see what the user chose, then based on that choice we change the value associated with that number we call the setting function in that class and assign it to the new function.
      try:
        if int(val)<1 and int(val)>4: print(Handler.out["out_of_bound_inp"])
        if int(val) == 1: obj.ncbi_api.set_retmax()
        if int(val) == 2: obj.set_max_acc() 
        if int(val) == 3: obj.tools.splitter.set_threshold()
        if int(val) == 4: obj.tools.set_bb()
      except: print("invalid choice :(")


  #welcome function that displays when handler class is first initialized. It allows the user to decide between whatever they'd like to to run and store it as a true or false in a list of booleans, then visually display that feedback back to the user. 
  @classmethod
  def welcome(cls,obj):
    #set everything to true initially as defaults, except the tree because it takes a long time if you have a lot of accessions
    path_list = [True,True,True,False]
    while True:
      #if itm in path_list is true, append an x to path-vals, otherwise a space.    
      path_vals = ['X' if itm  else ' ' for itm in path_list]
      #print out the feedback of the user/initial values based on the booleans in our list, which are shown to a user as an X for true or a space for false, as in, we're not running that.
      print(cls.out['welcome'].format(path_vals[0],path_vals[1],path_vals[2],path_vals[3]))
      #take the user's input
      inp = input("Value: ")
      #check if they want to leave this menu first, so that means they typed a quit statement or just hit enter
      if inp == "" or inp in ['quit','exit','q']: break
      #if you type advanced it pulls up the advanced menu, we have to pass our app object in there because we need to pull the data associated with the classes and subclasses.
      if inp == "advanced": cls.advanced_menu(obj)
      try:
        #we also have some predefined quality of life commands, 5 to say run everything, 6 to say run nothing and just give me the alignment and hte top 250 most similar accessions
        if int(inp)==5: path_list = [True for itm in path_list]
        elif int(inp)==6: path_list = [False for itm in path_list]
        #a human will input 4 for index 3 in our list, so we adjust for that. Then we toggle the switch on that choice, if true its now false, and vice versa. 
        else: path_list[int(inp)-1] = not path_list[int(inp)-1] 
      #we also define a statement for the user to tell them that their input was invalid
      except:
        print("Your input must be a valid integer between 1-6, an exit statement, or just an enter")
    cls.ex_check(inp)
    return cls(path_list)
