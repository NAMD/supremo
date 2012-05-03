# -*- coding:utf-8 -*-
'''
Created on Apr 18, 2012

@author: cyg
'''
import nltk
#from nltk.corpus.stopwords import words
from SENutils import senDbConn
#from SENutils import write_to_csv
from nltk import word_tokenize
from BeautifulSoup import BeautifulSoup as bfs
from isko_util import stopwords
import re
###############################################################################
#match_string1 = r"""unân[A-Z,a-z]{3,8}|unan[A-Z,a-z]{3,8}|UNÂN[A-Z,a-z]{3,8}|UNAN[A-Z,a-z]{3,8}|Unân[A-Z,a-z]{3,8}|Unan[A-Z,a-z]{3,8}"""
#match_string2 = r"""(?i)MAIORIA"""
###############################################################################
def find_re(texto, crex):
    """
    Retorna lista matches de expressao regular compilada "crex" em texto
    """
    matches = []
    #assert isinstance(texto, list)
    for t in texto:
        if not t:
            continue
        matches.extend(crex.findall(str(t)))
    return matches
###############################################################################
if __name__ == '__main__':
    db = senDbConn('Supremo_new', True)
    cursor = db.cursor()
    query = 'SELECT decisao FROM t_decisoes limit %s,%s'
    
    
    clean_tokens = []
     
    start_lim = -1
    end_lim = 100
    step = 10
        
    for moving_start_lim in range(start_lim,end_lim,step):
        clean_ementa_results = {}
        clean_decisao_results = {}
        
        rdy_query = query % (str(moving_start_lim+1),str(step))
        print rdy_query
        cursor.execute( rdy_query )
        result_tup = cursor.fetchall()
        
        count = 0
        for result in result_tup:
            if(count % 100 == 0):
                print count, ' ',
            decisao_texto = bfs(result[0].strip('[]'))#,  fromEncoding='ISO8859-1')
#            print '<H1>',count,'</H1>'
#            print '<br><H1>##################################################</H1><br>'
#            print decisao_texto.prettify()
#            ementa = decisao_texto.findAll('pre')   # A ementa esta envolta em uma marcacao HTML <pre> no texto da decisao
            strong_tags = decisao_texto.findAll('strong')
            for candidate_ementa_tag in strong_tags:
                clean_ementa = None
                if candidate_ementa_tag.text == 'Ementa':
                    clean_ementa = candidate_ementa_tag.parent.contents[-1]
                    clean_ementa_results[count] = str(clean_ementa)
            pre_tags = decisao_texto.findAll('pre')
            for candidate_decisao_tag in pre_tags:
                clean_decisao = None
                if candidate_decisao_tag.previous.previous == 'Decisão':
                    clean_decisao = candidate_decisao_tag.text
                    clean_decisao_results[count] = clean_decisao
                pass
            count += 1

        all_clean_texts = clean_decisao_results.values() + clean_ementa_results.values()
        all_tokens = []
        for text in all_clean_texts:
            all_tokens = all_tokens + word_tokenize(text)
        
#        compile_expr1 = re.compile("")
#        compile_expr2 = re.compile("")
#        compile_expr3 = re.compile("")
#        compile_expr4 = re.compile("")
#        compile_expr5 = re.compile("")
#        x = re.UNICODE
        print '\n\nall_tokens before clean_up:', len(all_tokens)
        
        for local_count in range(len(all_tokens)):
            try:
                try: local_token = all_tokens[local_count]
                except: break
                if not local_token: break
                
                ### 
                if "º" in all_tokens[local_count]:
                    all_tokens[local_count] = u'!AAA'
                ### 
                if "°" in all_tokens[local_count]:
                    all_tokens[local_count] = u'!AAA'
                ### 
                if "6.É" in all_tokens[local_count]:
                    all_tokens[local_count] = u'!AAA'
                ### 
                if "3.Daí" in all_tokens[local_count]:
                    all_tokens[local_count] = u'!AAA'
                ### 
                m = re.match(r"(\w+)\.", all_tokens[local_count])
                if m:
    #                print all_tokens[local_count]
                    x = unicode(all_tokens[local_count][0:-1])
                    all_tokens[local_count] = x
                ###
                p = re.match(r"(\d+)", all_tokens[local_count])
                if p: 
    #                    print ' ',all_tokens[local_count], 
                    all_tokens[local_count] = u'!AAA'
                ###
                n = re.match(r"(\d+)(\.)*", all_tokens[local_count])
                if n: 
    #                    print ' ',all_tokens[local_count], 
                    all_tokens[local_count] = u'!AAA'
                ###
                q = re.match(r"(\d+)/*", all_tokens[local_count])
                if q: 
    #                    print ' ',all_tokens[local_count], 
                    all_tokens[local_count] = u'!AAA'
                ###
                r = re.match(r"\-(\w+)*", all_tokens[local_count])
                if r: 
    #                    print ' ',all_tokens[local_count], 
                    all_tokens[local_count] = u'!AAA'
                ###
            except: 
                print 'ERROR AT TOKEN',all_tokens[local_count],' ...COUNT',local_count,'. CONTINUING.'
                continue
            
        print '\nall_tokens AFTER clean_up:', len(all_tokens)

        stemmer = nltk.stem.RSLPStemmer()
        clean_tokens = clean_tokens + [stemmer.stem(w.lower().strip()) for w in all_tokens if w.lower().strip() not in stopwords]
#        clean_tokens = clean_tokens + [w.lower().strip() for w in all_tokens if w.lower().strip() not in stopwords]
        start_lim = end_lim + 1

    fd = nltk.FreqDist(clean_tokens)
    xx = sorted(fd.items(), key=lambda num: num[1])[::-1]
#    write_to_csv('result/', 'result.csv', ('LEXEM','FREQ'), xx)
    cursor.close()
    pass