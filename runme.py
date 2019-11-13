#!/usr/bin/env python3
from app.app import App
from app.handler import Handler
from app.spinner import Spinner

def handle(obj,handler):
  handler.input_logic(obj)
  with Spinner("Generating summary "): obj.get_summary()
  if handler.proceed(obj.summary):
    with Spinner("Downloading data: "): obj.build_dataset()
    print("Species: ",obj.total_species(),"Accessions: ",obj.total_seqs())
    obj.align()
    if handler.path_list[0]:obj.plot()
    if handler.path_list[1]:obj.generate_motifs()
    #if handler.path_list[2]: obj.wildcard()
  else:
    return handle(obj,handler) 

def run_app():
  handler = Handler.welcome()
  app = App.from_class()
  handle(app,handler)

run_app()
