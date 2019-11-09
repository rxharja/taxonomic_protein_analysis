#!/usr/bin/env python3
from app.app import App
from app.handler import Handler
from app.spinner import Spinner

def handle(obj):
	handler.input_logic(obj)
	with Spinner("Generating summary "): obj.get_summary()
	if handler.proceed(obj.summary):
		with Spinner("Downloading data: "): obj.taxa()
		print("Species: ",obj.total_species(),"Accessions: ",obj.total_seqs())
		with Spinner("Writing fasta "): obj.write(obj.fasta)
		with Spinner("Building plot "): obj.plot()
	else:
		return handle(obj) 

app = App.from_class()
handler = Handler()
handle(app)
