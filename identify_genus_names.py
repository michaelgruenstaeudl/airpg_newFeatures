#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert scientific abstracts (i.e., text documents) to matrices of token 
counts and then using pairwise distances to find matches with keywords


# CURRENTLY FOR TESTING ONLY #
"""
__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>'
__info__ = 'Find genus names in abstracts using sklearn'
__version__ = '2022.02.20.1800'

##################################################
# IMPORT OPERATIONS #
#####################

import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from timeit import default_timer as timer
#from matplotlib import pyplot

##################################################
# READING INPUT #
#################
# Setting infiles
taxon_names_InFn = '_data_/Asteraecae_genera.txt'
scientific_abstracts_InFn = '_data_/abstracts_full.txt'

with open(taxon_names_InFn) as f:
    taxon_names = f.readlines()
taxon_names = ' '.join([n.strip('\n') for n in taxon_names])

with open(scientific_abstracts_InFn) as f:
    scientific_abstracts = f.read().split("\n\n\n")
scientific_abstracts = [re.sub("\d", " ", a) for a in scientific_abstracts]  # remove all digits
scientific_abstracts = [re.sub("[^a-zA-Z ]", " ", a) for a in scientific_abstracts]  # remove all special characters

##################################################
# FIND MATCHES #
################

def find_via_count_vectorizer(scientific_abstracts, taxon_names, verbose=False):
    ''' Function to find matches via sklearn's CountVectorizer '''
    results = []
    for idx,abstr in enumerate(scientific_abstracts):
        compare = [abstr, taxon_names]
        countVect = CountVectorizer()
        tokenCountMatrix = countVect.fit_transform(compare)
        cosSimAsPerc = cosine_similarity(tokenCountMatrix)[0][1] * 100
        if verbose:
            print("Abstract %s: %s%% matches with genus name list" % (str(idx), str(round(cosSimAsPerc, 2))))
        if cosSimAsPerc > 1.0:
            if verbose:
                print("    Abstract %s: Similarity greater than 1%%; saving to output ..." % (str(idx)))
            results.append(abstr)
            #names_list = countVect.get_feature_names_out()  # It's not printing out the actual matches
    return results


start = timer()
results_via_count_vectorizer = find_via_count_vectorizer(scientific_abstracts, taxon_names, verbose=False)
end = timer()
print("\nFinding matches via count vectorizer")
print("    Number of matching entries found:", len(results_via_count_vectorizer))
print("    Time elapsed:", round(end-start, 2))

##################################################
# EOF #
#######
