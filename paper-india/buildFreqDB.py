# -*- coding:utf-8 -*-
'''
Created on Apr 19, 2012

@author: cyg
'''
import nltk
from BeautifulSoup import BeautifulSoup as bfs
from nltk import word_tokenize
from isko_util import stopwords
from isko_util import clean_tokens
import gensim
from gensim import corpora
from SENutils import senDbConn
import logging
###############################################################################

###############################################################################
def extract_ementa_n_decisao_from_html(html):
    clean_ementa_results = ''
    clean_decisao_results = ''

    decisao_texto = bfs(html.strip('[]'))#,  fromEncoding='ISO8859-1')
    strong_tags = decisao_texto.findAll('strong')
    for candidate_ementa_tag in strong_tags:
        clean_ementa = None
        if candidate_ementa_tag.text == 'Ementa':
            clean_ementa = candidate_ementa_tag.parent.contents[-1]
            if clean_ementa:
                clean_ementa_results = str(clean_ementa)
    pre_tags = decisao_texto.findAll('pre')
    for candidate_decisao_tag in pre_tags:
        clean_decisao = None
        if candidate_decisao_tag.previous.previous == 'Decisão':
            clean_decisao = candidate_decisao_tag.text
            if clean_decisao:
                clean_decisao_results = clean_decisao
        pass
    all_clean_text = clean_decisao_results + clean_ementa_results
    return all_clean_text

###############################################################################
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    supremo_conn = senDbConn('Supremo_new', True)
    all_tokens = set()
    supr_cursor = supremo_conn.cursor()
    query = 'SELECT id_processo,decisao,data_decisao FROM t_decisoes WHERE year(data_decisao) = %s'
    START_YEAR = 1988
    END_YEAR = 1990
    
    dictionary = corpora.Dictionary()
    corpus = []
    for year in range(START_YEAR,END_YEAR):
        print 'starting',year
        supr_cursor.execute(query % (year))
        result_tup = supr_cursor.fetchall()
        count = 0
        for result in result_tup:
            save_every = len(result_tup) // 4
            count += 1
            print count,
#            try:
            text = extract_ementa_n_decisao_from_html(result[1])
            tokens = word_tokenize(text)
            cleaned_tokens = clean_tokens(tokens)
            cleaned_tokens = [w.lower().strip() for w in cleaned_tokens if w.lower().strip() not in stopwords]
            stemmed_tokens = []
            
            #gensim code
            new_vec = dictionary.doc2bow(cleaned_tokens, allow_update=True)
            corpus.append(new_vec)
            if count % save_every == 0:
                print 'saving ...',
                dictionary.save('gensim-data/dicts/'+str(year)+'_partial_dictionary_'+str(count)+'.dict')
                corpora.MmCorpus.serialize('gensim-data/corpora/'+str(year)+'_partial_corpus_'+str(count)+'.mm', corpus)
                print 'done'
#            except:
#                print 'error found in decision whose case is:', result[0]  
#                continue
        # last save when processing is done
        print 'LAST SAVE ...',
        dictionary.save('gensim-data/dicts/' + str(year) + '_full_dictionary_.dict')
        corpora.MmCorpus.serialize('gensim-data/corpora/' + str(year) + '_full_corpus_.mm', corpus)
        print 'done'
        lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, update_every=1, chunksize=10000, passes=1)
        lda.save('gensim-data/models/'+str(year)+'_model.pickle')
        lda.show_topics(20)
    supr_cursor.close()      
    pass
###############################################################################

