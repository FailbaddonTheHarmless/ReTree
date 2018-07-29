# -*- coding: utf-8 -*-
"""

@author: Dave
"""
import itertools
import csv

def load_csv(re_file):
    regexps = []
    with open(re_file, newline='') as csvfile:
        re_reader = csv.reader(csvfile, delimiter=',')
        for row in re_reader:
            regexps.extend(row)
    return regexps

def generate_alternatives(options):
        result = (''.join(w) for w in itertools.combinations(options, 2))
        alternatives = ('(' + r[-2] + '|' + r[-1] + ')' for r in result)
        
        return alternatives