# -*- coding:utf-8 -*-
'''
Created on Apr 3, 2012

@author: cyg
'''
from SENutils import senDbConn
from SENutils import STATE_KEYS
from SENutils import write_to_csv
from datetime import *
###################################################################################################
#prequery = """select PROCESSO.seq_objeto_incidente,PROCESSO.num_processo, PROCESSO.sig_classe_proces, ANDAMENTO_PROCESSOS.num_sequencia, PROCESSO.dat_autuacao, ANDAMENTO_PROCESSOS.dat_andamento, ANDAMENTOS.dsc_andamento
prequery = """select PROCESSO.dat_autuacao, ANDAMENTO_PROCESSOS.dat_andamento
from PROCESSO, ANDAMENTOS, ANDAMENTO_PROCESSOS, HISTORICO_PROCESSO_ORIGEM
where PROCESSO.num_processo = ANDAMENTO_PROCESSOS.num_processo
and PROCESSO.sig_classe_proces = ANDAMENTO_PROCESSOS.sig_classe_proces
and ANDAMENTO_PROCESSOS.cod_andamento = ANDAMENTOS.cod_andamento
and HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente = PROCESSO.seq_objeto_incidente
and HISTORICO_PROCESSO_ORIGEM.cod_procedencia = %s
and ANDAMENTOS.DSC_ANDAMENTO in
(
    select DSC_ANDAMENTO from ANDAMENTOS where DSC_ANDAMENTO like '%%publica%%'
)
and ANDAMENTOS.cod_andamento <> 1056 
and ANDAMENTOS.cod_andamento <> 1058
and ANDAMENTOS.cod_andamento <> 1060
and ANDAMENTOS.cod_andamento <> 1061
and ANDAMENTOS.cod_andamento <> 1063
and ANDAMENTOS.cod_andamento <> 1112
and ANDAMENTOS.cod_andamento <> 1113
and ANDAMENTOS.cod_andamento <> 1114
and ANDAMENTOS.cod_andamento <> 2053
and ANDAMENTOS.cod_andamento <> 2101
and ANDAMENTOS.cod_andamento <> 4050
and ANDAMENTOS.cod_andamento <> 4140
and ANDAMENTOS.cod_andamento <> 7910
and ANDAMENTOS.cod_andamento <> 7911
and ANDAMENTOS.cod_andamento <> 7912
and ANDAMENTOS.cod_andamento <> 7913
and ANDAMENTOS.cod_andamento <> 7914
and ANDAMENTOS.cod_andamento <> 7915
and ANDAMENTOS.cod_andamento <> 8451
and ANDAMENTOS.cod_andamento <> 8503
and year(dat_autuacao) >= 2000
and year(dat_autuacao) <= 2009
group by PROCESSO.num_processo, PROCESSO.sig_classe_proces
order by num_sequencia desc
limit 10000000"""
###################################################################################################
def run():
    db = senDbConn(flagRemoteSSH=False)
    cursor = db.cursor()
    all_state_avgs = {}
    for code in STATE_KEYS.items():
        query_pronta = prequery % code[1]
        cursor.execute( query_pronta )
        result_tup = cursor.fetchall()
        state_avg = extract_avg_time(result_tup, code[0])
        
        all_state_avgs[code[0]] = state_avg
    write_to_csv('dados/', 'consolidado.csv', ('UF','Duração'), all_state_avgs.items())
###################################################################################################
def extract_avg_time(result_tup, state_code):
    over = len(result_tup)
    totaldays = None
    over365 = 0
    for result in result_tup:

       # start = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
       # end = datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S")
        minus = result[1] - result[0]
        # minus = end - start
        if minus.days > 365:
            over365 += 1
        else:
            over365 -= 1 
        if totaldays is None: totaldays = minus
        else: totaldays += minus
    avgTOTALdays =  totaldays.days / over
    avgyear = avgTOTALdays // 365.25
    left = avgTOTALdays % 365.25
    avgmonth = left // 30
    avgday = left % 30
    #print 'MINUS HERE:', over365
    print state_code, 'has avg', avgyear, 'years,', avgmonth, 'months, and', avgday, 'days'
    return (avgTOTALdays)
###################################################################################################
if __name__ == '__main__':
    run()
    pass
