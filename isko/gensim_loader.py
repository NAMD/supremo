'''
Created on Apr 20, 2012

@author: cyg
'''
import gensim
import logging
from gensim import corpora
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#from SENutils import write_to_csv
from SENutils import load_csv
if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
    csv_mapping = load_csv('gensim-data/csvmapping500.csv')
    mydict = corpora.dictionary.Dictionary.load('gensim-data/dicts/3year_full_bigram_dictionary.dict')
    corpus = corpora.mmcorpus.MmCorpus('gensim-data/corpora/3year_full_bigram_corpus.mm')
#    mydict = corpora.dictionary.Dictionary.load('gensim-data/dicts_old/1990_full_bigram_dictionary.dict')
#    corpus = corpora.mmcorpus.MmCorpus('gensim-data/corpora_old/1990_full_bigram_corpus.mm')
    print 'DICT'
    print mydict
    print 'CORPUS'
    print corpus
    checker = set()
    for doc in corpus:
        checker.add(tuple(doc))
    print len(checker)
    lsi = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=mydict, num_topics=10)
    lsi.show_topics(num_topics=-1, num_words=10, log=False, formatted=True)
    corpus_lsi = lsi[corpus]
    listt = []
    
    for tup in zip(corpus_lsi, csv_mapping[1:]):
        listt.append( (tup[1][1],tup[1][2],tup[1][3],tup[1][4],tup[0]) )
#    write_to_csv('gensim-data/','3year_coords_full_24k_new.csv', ('',''), listt)
######
di = {}
######
def check(doc):
    if not di.get(doc[0]):
        return False
######
def rec(a, b):
    if not a[0] == b[0]: return False
    if not a[1] == b[1]: return False
    return True
    
    
    
 