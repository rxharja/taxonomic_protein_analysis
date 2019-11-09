#!/usr/bin/env python3
from app.app import App
from app.handler import Handler

def handle(obj):
	handler.input_logic(obj)
	obj.get_summary()
	print(obj.summary)
	if handler.proceed(obj.summary):
		obj.taxa()
		print("Species: ",obj.total_species(),"Accessions: ",obj.total_seqs())
		print("writing fasta")
		obj.write(obj.fasta)
		obj.plot()
	else:
		return handle(obj) 

app = App.from_class()
handler = Handler()
handle(app)
