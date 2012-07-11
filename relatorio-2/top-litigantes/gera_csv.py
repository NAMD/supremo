# coding: utf-8
'''
Created on Jul 6, 2012

@author: cyg
'''
from SENutils import load_csv, deleta_e_cria_diretorio
from SENutils import write_to_csv
from SENutils import STATE_CODES
from SENutils import deleta_e_cria_diretorio
import operator
import plotter

LIMIT_TO = 10

def run():
    l_proc_uf = load_csv("csv/TEMP_PROC_UF_ANO.csv")
#    ['8061', 'AC', '2009']
    yearlydata = {}
#    yearlydata = { <UF>:{ NOME:[QTD1,QTD2,...] } }
    data = {}
#    data = {<UF>:{NOME:QTD}}}
    tmp1 = {}
#    { <PROC>:[<UF>,<ANO>] }
    count = 0
    for proc in l_proc_uf[1:]:
        if tmp1.get(proc[0]):
            count += 1; print count, 'weird, already exists? shouldnt happen -', proc
        else:
            if int(proc[2]) >= 2000 and int(proc[2]) <= 2009 and not '*' in proc[1]:
                tmp1[proc[0]] = [proc[1],int(proc[2])]
    for state_code in STATE_CODES.values():
        data[state_code] = {}
        for yr in range(2000, 2010):
            yearlydata[state_code] = {}
        
        
    l_proc_names = load_csv("csv/TEMP_PROC_NOM_LIT.csv")
#    ['8089', 'MARIZA PETERLINI']
    valid_cases = 0
    invalid_cases = 0
    for proc_lit_list in l_proc_names:
        lit_name = mapit(proc_lit_list[1])
        proc_id = proc_lit_list[0]
        
        if not tmp1.get(proc_id):
            invalid_cases += 1
            continue
        valid_cases += 1; 
        uf = tmp1[proc_id][0]
        yr = tmp1[proc_id][1]
        if data[uf].get(lit_name):
            data[uf][lit_name] = data[uf][lit_name] + 1
        else:
            data[uf][lit_name] = 1
#            m
        idx = yr-2000
        if yearlydata[uf].get(lit_name):
            if yearlydata[uf][lit_name][idx]:
                yearlydata[uf][lit_name][idx] = yearlydata[uf][lit_name][idx] + 1
            else:
                yearlydata[uf][lit_name][idx] = 1
        else:
            yearlydata[uf][lit_name] = [None] * 10
            yearlydata[uf][lit_name][idx] = 1
            
    print 'out. valid:', valid_cases, 'invalid:', invalid_cases
    
    finaldata = {}
    finalyearlydata = {}
    deleta_e_cria_diretorio("top_litigantes_por_uf/dados")
    deleta_e_cria_diretorio("top_litigantes_por_uf_ano/dados")
    for data_item in data.items():
        uf = data_item[0]
        qties_by_name = data_item[1]
        finaldata[uf] = sorted(qties_by_name.iteritems(), key=operator.itemgetter(1), reverse=True)
        write_to_csv("top_litigantes_por_uf/dados/", uf+'.csv', ('litigante','processos'),finaldata[uf][0:LIMIT_TO])
        
#        for name_n_yrly_qty_list in yearlydata[uf].items(): # { NOME:[QTD1,QTD2,...] } 
#            yrly_qty_list = name_n_yrly_qty_list[1]
        for name_n_proc in finaldata[uf][0:LIMIT_TO]:
            name_to_fetch = name_n_proc[0]
            if not finalyearlydata.get(uf):
                x = yearlydata[uf][name_to_fetch]
                x.insert(0, name_to_fetch)
                y = [i if i != None else 0 for i in x]
                finalyearlydata[uf] = [y]
            else:
                x = yearlydata[uf][name_to_fetch]
                x.insert(0, name_to_fetch)
                y = [i if i != None else 0 for i in x]
                finalyearlydata[uf].append( y )
        write_to_csv("top_litigantes_por_uf_ano/dados/"
             , uf+".csv"
             , ("nome","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009")
             , finalyearlydata[uf])
            
    
    pass
###################################################################################################
mapable_names = {"INSTITUTO NACIONAL DO SEGURO SOCIAL - INSS":"INSS",
     "CAIXA ECONOMICA FEDERAL - CEF":"CEF"
    }
mapable_words = {u"secretaria":"SEC", u"estado":"EST", u'sindicato':'SIND', u'indústria':'IND'
                 , u'secretário':'SEC', u'secretária':'SEC', u'governo':'GOV', u'federal':'FED'
                 , u'procurador':'proc', u'procuradoria':'proc', u'ministério':'MIN'
                 , u'presidente':'PRES', u'TRIBUNAL':'TRIB', u'justiça':'JUS', u'federais':'FED'
                 , u'município':'MUN', u'municípios':'MUN', u'companhia':'CIA'
                 , u'universidade':'UNIV', u'superior':'SUP', u'público':'PUB'
    }
###################################################################################################
def mapit(name):
#    if mapable_names.get(name): return mapable_names[name]
    if " - " in name:
        return name[name.rindex(" - ")+3:]
    name = unicode(name)
    for state_name in STATE_CODES.keys():
        if state_name in name.lower():
            name = name.replace(state_name.upper(), unicode(STATE_CODES[ state_name ]))
            break
    for token in name.split(' '):
#        token = token.decode('utf-8')
        token = unicode(token)
        if token.lower() in mapable_words:
            name = name.replace(token, mapable_words[token.lower()])
    return name
###################################################################################################
def plotit():
    pass
###################################################################################################
if __name__ == '__main__':
#    print mapit("ESTADO DE MINAS GERAIS")
    run()
    pass