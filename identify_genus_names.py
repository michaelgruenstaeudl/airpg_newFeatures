#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert scientific abstracts (i.e., text documents) to matrices of token 
counts and then using pairwise distances to find matches with keywords


# CURRENTLY FOR TESTING ONLY #
"""
__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>'
__info__ = 'Find genus names in abstracts using sklearn'
__version__ = '2022.02.20.1830'

##################################################
# IMPORT OPERATIONS #
#####################

import matplotlib.pyplot as plt
import pandas as pd
import re
from timeit import default_timer as timer
import tracemalloc
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

##################################################
# FUNCTIONS #
#############
def load_and_preprocess(family_name):
    ''' Function to find matches via sklearn's CountVectorizer '''
    genus_names_InFn = '_data_/'+family_name+'_genera.txt'
    scientific_abstracts_InFn = '_data_/'+family_name+'_abstracts_full.txt'
    # Load taxon names
    with open(genus_names_InFn) as f:
        genus_names = f.readlines()
    genus_names = ' '.join([n.strip('\n') for n in genus_names])
    # Load scientific abstracts
    with open(scientific_abstracts_InFn) as f:
        scientific_abstracts = f.read().split("\n\n\n")
    scientific_abstracts = [re.sub("\d", " ", a) for a in scientific_abstracts]  # remove all digits
    scientific_abstracts = [re.sub("[^a-zA-Z ]", " ", a) for a in scientific_abstracts]  # remove all special characters
    return [genus_names, scientific_abstracts]

def find_via_count_vectorizer(scientific_abstracts, genus_names, verbose=False):
    ''' Function to find matches via sklearn's CountVectorizer '''
    results = []
    for idx,abstr in enumerate(scientific_abstracts):
        compare = [abstr, genus_names]
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

def exec_via_count_vectorizer(family_name, genus_names, scientific_abstracts):
    ''' Wrapper function to find matches via sklearn's CountVectorizer '''
    print("Finding matches via count vectorizer for %s" % (family_name))
    time_start = timer()  # Start time monitoring
    tracemalloc.start()  # Start memory monitoring
    results = find_via_count_vectorizer(scientific_abstracts, genus_names, verbose=False)
    time_end = timer()  # End time monitoring
    results_n = len(results)
    results_mem = tracemalloc.get_traced_memory()[1] // 1048576
    tracemalloc.stop()  # Stop memory monitoring
    results_time = round(time_end-time_start, 2)
    print("    Number of matching entries found: %s" % (results_n))
    print("    Memory used at peak: %s MiB" % (results_mem))
    print("    Time elapsed: %s sec." % (results_time))
    return [results_n, results_mem, results_time]

##################################################
# MAIN #
########

family_names_InFn = '_data_/short_list_families.txt'  # '_data_/list_angiosperm_families.txt'
with open(family_names_InFn) as f:
    family_names = f.readlines()
family_names = [n.strip('\n') for n in family_names]

df = pd.DataFrame(columns=['Family', 'N_Abstracts', 'N_Matches', 'Peak_MEM', 'Time'])
for idx,fam in enumerate(family_names):
    genus_names, scientific_abstracts = load_and_preprocess(fam)
    results_n, results_mem, results_time = exec_via_count_vectorizer(fam, genus_names, scientific_abstracts)
    values_to_add = {
        'Family': fam,
        'N_Abstracts': len(scientific_abstracts),
        'N_Matches': results_n,
        'Peak_MEM': results_mem,
        'Time': results_time
    }
    row_to_add = pd.Series(values_to_add, name=idx)
    df = df.append(row_to_add)


##################################################
# PLOTTING #
############

plt.figure(figsize=(18,4))
plt.bar(df["Family"], df["N_Matches"])
plt.ylabel("Number of matches")
plt.xticks(rotation=90)
plt.savefig('figure_matches.png', bbox_inches='tight')

plt.figure(figsize=(18,4))
plt.bar(df["Family"], df["Time"], color = "red")
plt.ylabel("Calculation time")
plt.xticks([])
plt.savefig('figure_time.png', bbox_inches='tight')

plt.figure(figsize=(18,4))
plt.bar(df["Family"], df["Peak_MEM"], color = "green")
plt.ylabel("Peak memory")
plt.xticks([])
plt.savefig('figure_mem.png', bbox_inches='tight')

##################################################
# EOF #
#######
