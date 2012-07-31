# -*- coding:utf-8 -*-
'''
Created on Apr 19, 2012

@author: cyg
'''
import nltk

from nltk import word_tokenize
import isko_util
from gensim import corpora
from SENutils import senDbConn
import logging
###############################################################################
# building a GENSIM dictionary and corpus based on a database query.
# using beautifulsoup to clean HTML content 
###############################################################################
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    supremo_conn = senDbConn('Supremo_new')
    supr_cursor = supremo_conn.cursor()
    query = 'SELECT id_processo,decisao,data_decisao FROM t_decisoes WHERE year(data_decisao) = %s'
    
    all_tokens = set()
    START_YEAR = 2005
    END_YEAR = 2009
    mydict = corpora.Dictionary()
    corpus = []

    for year in range(START_YEAR,END_YEAR):
        print 'starting',year
        supr_cursor.execute(query % (year))
        result_tup = supr_cursor.fetchall()
        count = 0
        for result in result_tup:
            if len(result_tup) > 2000: save_every = len(result_tup) // 4
            else: save_every = len(result_tup)
            count += 1
            if count % 100 == 0:
                print count,
#            try:
            text = isko_util.extract_ementa_n_decisao_from_html(result[1])
            tokens = word_tokenize(text)
            cleaned_tokens = isko_util.clean_tokens(tokens)
            cleaned_tokens = [w.lower().strip() for w in cleaned_tokens if w.lower().strip() not in isko_util.stopwords]
            bigrams = nltk.bigrams(cleaned_tokens)
            cleaned_bigrams = 
            bigramstrings = map(lambda x: ' '.join(x), bigrams)
            stemmed_tokens = []
            
            #gensim code
            new_vec = mydict.doc2bow(bigramstrings, allow_update=True)
            corpus.append(new_vec)
            if count % save_every == 0:
                print 'saving ...',
                mydict.save('gensim-data/dicts/'+str(year)+'_partial_bigram_dictionary_'+str(count)+'.dict')
                corpora.MmCorpus.serialize('gensim-data/corpora/'+str(year)+'_partial_bigram_corpus_'+str(count)+'.mm', corpus)
                print 'done'
#            except:
#                print 'error found in decision whose case is:', result[0]  
#                continue
        # last save when processing is done
        print 'LAST SAVE ...',
        print 'done'

#        lsi = gensim.models.lsimodel.LsiModel()
    supr_cursor.close()      
    pass
###############################################################################

