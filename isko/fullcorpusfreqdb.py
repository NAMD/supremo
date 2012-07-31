# -*- coding:utf-8 -*-
'''
Created on Apr 19, 2012

@author: cyg
'''

import nltk
#from nltk import word_tokenize
from isko_util import stopwords
from isko_util import clean_tokens
from isko_util import extract_ementa_n_decisao_from_html
#from gensim import corpora
from SENutils import senDbConn
from SENutils import write_to_csv
import logging
from isko_util import bi_stopwords
import re


if __name__ == '__main__':
    bag_of_ids = set()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    supremo_conn = senDbConn('Supremo_new', True)
    all_tokens = set()
    supr_cursor = supremo_conn.cursor()
    limit = 100
    query = """SELECT t_processos.id_processo, t_decisoes.decisao, year(t_decisoes.data_decisao), t_processos.relator, t_processos.proc_class
        FROM t_decisoes, t_processos
        WHERE t_decisoes.id_processo = t_processos.id_processo
        and year(data_decisao) = %s
        group by t_processos.id_processo
        limit %s"""


    START_YEAR = 2000
    END_YEAR = 2001

    all_results = []
    for year in range(START_YEAR, END_YEAR):
        print 'starting ...',year,
        supr_cursor.execute( query % (str(year),str(limit) ) )
        yearly_result_tup = supr_cursor.fetchall()
        all_results = all_results + list(yearly_result_tup)
        print  'done'

#    mydict = corpora.Dictionary()
#    corpus = []

    count = 0

    print 'writing ...',
    y = list(all_results)
    to_csv = zip( range(len(all_results)), map(lambda x: x[0],y) , map(lambda x: x[2],y) , map(lambda x: x[3],y) , map(lambda x: x[4],y) )
    write_to_csv('gensim-data/csv/', 'mapping'+str(len(all_results))+'.csv', ('ID','ANO','RELATOR','CLASSE'), to_csv)
    print 'done'

    texts = []

    for result in all_results:
        if len(all_results) > 2000: save_every = len(all_results) // 4
        else: save_every = len(all_results)
        count += 1
        if count % 100 == 0:
            print count,
        if result[0] not in bag_of_ids: bag_of_ids.add(result[0])
        else:  continue
        ementa,decisao = extract_ementa_n_decisao_from_html(result[1])
#        texts.append(text)
#        tokens = word_tokenize(text)
        regexp = re.compile('[ ,.\r\n\t]')
        tokens = regexp.split(ementa) + regexp.split(decisao)

        cleaned_tokens = clean_tokens(tokens)
        cleaned_tokens = [w.lower().strip() for w in cleaned_tokens if w.lower().strip() not in stopwords]
        bigrams = nltk.bigrams(cleaned_tokens)
        bigrams = [w for w in bigrams if w not in bi_stopwords]
        bigramstrings = map(lambda x: ' '.join(x), bigrams)
        texts.append( bigramstrings, )
        #gensim code
#        new_vec = mydict.doc2bow(bigramstrings, allow_update=True)
#        corpus.append(new_vec)
        if count % save_every == 0 and save_every != count:
            print 'saving partial...',
            to_csv = zip( range(len(all_results)), map(lambda x: x[0],y) , map(lambda x: x[2],y) , map(lambda x: x[3],y) , map(lambda x: x[4],y), texts )
            write_to_csv('gensim-data/csv/', 'partial_mapping'+count+'_WITH_BIGRAMS.csv', ('ID','ANO','RELATOR','CLASSE'), to_csv)
#            mydict.save('gensim-data/dicts/3year_partial_bigram_dictionary_'+str(count)+'.dict')
#            corpora.MmCorpus.serialize('gensim-data/corpora/3year_partial_bigram_corpus_'+str(count)+'.mm', corpus)
            print 'done'
    # last save when processing is done
#    write_to_csv('gensim-data/','texts.csv',('nuthin'), texts)

    print 'LAST SAVE ...',
    to_csv = zip( range(len(all_results)), map(lambda x: x[0],y) , map(lambda x: x[2],y) , map(lambda x: x[3],y) , map(lambda x: x[4],y), texts )
    write_to_csv('gensim-data/csv', 'full_mapping_WITH_BIGRAMS.csv', ('ID','ANO','RELATOR','CLASSE'), to_csv)
#    mydict.save('gensim-data/dicts/3year_full_bigram_dictionary.dict')
#    corpora.MmCorpus.serialize('gensim-data/corpora/3year_full_bigram_corpus.mm', corpus)
    print 'done'

    supr_cursor.close()
