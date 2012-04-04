# -*- coding:utf-8 -*-
'''
Created on Jan 23, 2012

@author: cyg
'''
from SENutils import load_csv
from SENutils import write_to_csv

def run():
    classMapping = load_csv('csv/misc/tipoDeCortePorCLASSE.csv')
    classByState = load_csv('csv/misc/classePorEstado_POR_ANO.csv')
    mapping = dict( (v.strip(),k) for k,v in classMapping )
    pass
    final = {}
    # ass = mapping["AÇÃO CAUTELAR"]
    for state, year, classe, num in classByState[1:]:
        if not final.get(state):
            final[state] = {}
        if not final[state].get(mapping[classe]):
            final[state][mapping[classe]] = 0
        final[state][mapping[classe]] = final[state][mapping[classe]] + int(num)
        for k,v in final.iteritems():
            write_to_csv("csv/misc/tipoDeCortePorEstadoPorAno/",k+"_tipoDeCorte.csv",["tipo de corte","qtde processos"], v.items())
        
        
        
if __name__ == '__main__':
    run()
    pass