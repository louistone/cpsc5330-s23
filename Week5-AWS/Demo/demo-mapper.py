#!/usr/bin/python3

import sys
import os
import re

def tokenize(text):
    text = text.lower().replace('_', ' ')
    words = re.findall(r'\b\w+\b', text)    
    words = [word for word in words if word != ""]
    return words

for line in sys.stdin:
#    docid = os.path.splitext(os.path.basename(os.getenv('map_input_file')))[0]
   words = tokenize(line)
   for word in words:
#       print('%s\t%s' % (docid, word)) 
       print('%s\t%s' % (1, word))
