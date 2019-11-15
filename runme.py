#!/usr/bin/env python3
from app.app import App
from handler.handler import Handler
from app.spinner import Spinner

def handle(obj,handler):
  handler.input_logic(obj)
  with Spinner("Generating summary "): obj.get_summary()
  if handler.proceed(obj.summary):
    with Spinner("Downloading data "): 
      obj.build_dataset()
      obj.get_fasta()
    if handler.count_results(obj.total_seqs(),obj.total_species()):
      obj.process_redundant()
      if handler.count_results(obj.total_seqs(),obj.total_species()):
        obj.align()
        if handler.path_list[0]:obj.plot()
        if handler.path_list[1]:print(obj.generate_motifs())
        if handler.path_list[2]: obj.tree()
    else:
      return handle(obj,handler)
  else:
    return handle(obj,handler) 

def run_app():
  handler = Handler.welcome()
  app = App.from_class()
  handle(app,handler)

run_app()
