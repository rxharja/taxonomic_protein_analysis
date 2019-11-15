#!/usr/bin/env python3
from app.app import App
from handler.handler import Handler
from app.spinner import Spinner

def handle(obj,handler):
  handler.input_logic(obj)
  with Spinner("Generating summary "): obj.get_summary()
  if not handler.proceed(obj.summary): return handle(obj,handler)
  with Spinner("Downloading data "): 
    obj.build_dataset()
    obj.get_fasta()
  if not handler.count_results(obj.total_seqs(),obj.total_species()): return handle(obj,handler)
  if handler.path_list[0]: 
    obj.process_redundant()
    if not handler.count_results(obj.total_seqs(),obj.total_species()): return handle(obj,handler)
  obj.align()
  if handler.path_list[1]:obj.plot()
  if handler.path_list[2]:print(obj.generate_motifs())
  if handler.path_list[3]: obj.tree()
  obj.file_locs()

def run_app():
  handler = Handler.welcome()
  app = App.from_class()
  handle(app,handler)

run_app()
