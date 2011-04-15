#!/usr/bin/env python2.6
import pprint
pp = pprint.PrettyPrinter(indent=4)
cond_prob = {
        'a':{'h1':0.8, 'h2':0.25, 'h3':0.5},
        'b':{'h1':0.8, 'h2':0.75, 'h3':0.5},
        'c':{'h1':0.2, 'h2':0.75, 'h3':0.5},
        }
pp.pprint(cond_prob)
instances=[('a','+'), ('b', '-'), ('c', '+')]
