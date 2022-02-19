#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert scientific abstracts (i.e., text documents) to matrices of token 
counts and then using pairwise distances to find matches with keywords


# CURRENTLY FOR TESTING ONLY #
"""
__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>'
__info__ = 'Find keywords in abstracts using machine learning'
__version__ = '2022.02.19.2000'

##################################################
# IMPORT OPERATIONS #
#####################

import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from matplotlib import pyplot

##################################################
# READING INPUT #
#################
# Setting infiles
taxon_names_InFn = 'data/Asteraecae_genera.txt'
scientific_abstracts_InFn = 'data/abstracts_full.txt'

with open(taxon_names_InFn) as f:
    taxon_names = f.readlines()
taxon_names = ' '.join([n.strip('\n') for n in taxon_names])

with open(scientific_abstracts_InFn) as f:
    scientific_abstracts = f.read().split("\n\n\n")
scientific_abstracts = [re.sub("\d", "", s) for s in scientific_abstracts]  # remove all digits
scientific_abstracts = [re.sub("[^a-zA-Z ]", "", s) for s in scientific_abstracts]  # remove all special characters

##################################################
# FIND MATCHES #
################

for idx,abstr in enumerate(scientific_abstracts):
    compare = [abstr, taxon_names]
    countVect = CountVectorizer()
    tokenCountMatrix = countVect.fit_transform(compare)
    cosSimAsPerc = cosine_similarity(tokenCountMatrix)[0][1] * 100
    if cosSimAsPerc > 1.0:
        print("Abstract %s contains %s%% of all genus names" % (idx, str(round(cosSimAsPerc, 2))))
        names_list = countVect.get_feature_names_out()

        # It's not printing out the actual matches

        print(names_list[0:10])


##################################################
# EOF #
#######
