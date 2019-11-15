#!/usr/bin/env python3
import subprocess

class Tree:
  
  def init(alignment_file):
    self.alignment_file = alignment_file
    self.bb = 1000
    self.path = "./outputs/tree/"
 
 
  def build_tree(self):
    subprocess.call('iqtree -s {} -bb {} -pre {} -quiet'.format(self.alignment_file,self.bb,self.path),shell=True)
