'''
Created on Apr 25, 2012

@author: cyg
'''
from SENutils import senDbConn
from isko_util import extract_ementa_n_decisao_from_html
from isko_util import stopwords
import re

def run():
    query = """SELECT decisao from t_decisoes limit %s,%s"""
    start_lim = 0
    step = 10
    end_lim = 50
    conn = senDbConn("Supremo_new")
    cursor = conn.cursor()
    
    for moving_start_lim in range(start_lim,end_lim,step):
        clean_ementa_results = {}
        clean_decisao_results = {}
        
        rdy_query = query % (str(moving_start_lim+1),str(step))
#        print rdy_query
        cursor.execute( rdy_query )
        result_tup = cursor.fetchall()
        token_set = set()
        
        doc_tokenbag = set()
        doc_tokendict = {}
        for tup in result_tup:
            (ementa,decisao) = extract_ementa_n_decisao_from_html(tup[0])
            regexp = re.compile('[ ,.\r\n\t]')
            ementa_tok = regexp.split(ementa)
            decisao_tok = regexp.split(decisao)
            all_tokens = decisao_tok + ementa_tok 
#            all_tokens_str = ' '.join([x for x in ementa_tok if x]) + ' '.join([y for y in decisao_tok if y])
            print '###########################################################' 
            print ementa
            for x in all_tokens:
                if x in stopwords: continue
                if x in doc_tokenbag:
                    update_count(doc_tokendict, x)
                else:
                    doc_tokenbag.add(x)
                    doc_tokendict[x] = 1
                    pass
###############################################################################
def update_count(dictt, lexem):
        dictt[lexem] = dictt[lexem] + 1
###############################################################################
if __name__ == '__main__':
    run()    
    pass