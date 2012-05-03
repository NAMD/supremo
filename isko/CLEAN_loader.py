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
from SENutils import write_to_csv
from SENutils import load_csv
###############################################################################
def extract(tup):
    coords = tup[5].strip('[]').split('\', u\'')
    if len(coords) == 1:
        coords = tup[5].strip('[]').split('\', \'')
    
    coords[0] = coords[0].strip('u\'')
    coords[-1] = coords[-1].strip('\'')
    if len(coords) == 1:
        print coords
        return None
    res = (
            int(tup[0])
            ,int(tup[1])
            ,tup[2]
            ,tup[3]
            ,tup[4]
            ,tuple(coords)
            )
#    print clean_coords
    return res
###############################################################################
if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
    csv_mapping = load_csv('gensim-data/csvmapping24K_WITH_BIGRAMS.csv', encoding='unicode')
    clean_bigrams = map(extract, csv_mapping[1:])
    check_set = set()
    clean_corpus = []
    
    mydict = corpora.Dictionary()
    corpus = []
    
    for item in clean_bigrams:
        if item and item[5] not in check_set:
            check_set.add(item[5])
            clean_corpus.append(item)
            new_vec = mydict.doc2bow(item[5], allow_update=True)
            corpus.append(new_vec)
    
#    mydict.save('gensim-data/dicts/3year_full_bigram_dictionary.dict')
#    corpora.MmCorpus.serialize('gensim-data/corpora/3year_full_bigram_corpus.mm', corpus)
    lsi = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=mydict, num_topics=10)
    lsi.show_topics(num_topics=-1, num_words=10, log=False, formatted=True)
    corpus_lsi = lsi[corpus]
    listt = []
    
    for tup in zip(corpus_lsi, clean_corpus):
        listt.append( (tup[1][1],tup[1][2],tup[1][3],tup[1][4],tup[0]) )
    write_to_csv('gensim-data/','3year_coords_full_CLEAN.csv', ('',''), listt)
 
    
 