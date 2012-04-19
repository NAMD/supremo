'''
Created on Apr 11, 2012

@author: cyg
'''
import numpy as np
import matplotlib as mp
from statlib import stats
from SENutils import senDbConn
from SENutils import STATE_KEYS
from SENutils import write_to_csv
from datetime import *
###################################################################################################
query = """select PROCESSO.SEQ_OBJETO_INCIDENTE, DAT_AUTUACAO,DAT_ANDAMENTO
from PROCESSO, ANDAMENTOS, ANDAMENTO_PROCESSOS
where PROCESSO.num_processo = ANDAMENTO_PROCESSOS.num_processo
and PROCESSO.sig_classe_proces = ANDAMENTO_PROCESSOS.sig_classe_proces
and ANDAMENTO_PROCESSOS.cod_andamento = ANDAMENTOS.cod_andamento
and (
    PROCESSO.SIG_CLASSE_PROCES = 'ADI'
    or PROCESSO.SIG_CLASSE_PROCES = 'ADO'
    or PROCESSO.SIG_CLASSE_PROCES = 'ADC'
    or PROCESSO.SIG_CLASSE_PROCES = 'ADPF'
)
and 
(
    ANDAMENTOS.COD_ANDAMENTO = 1020
    or ANDAMENTOS.COD_ANDAMENTO = 1021
    or ANDAMENTOS.COD_ANDAMENTO = 1022
    or ANDAMENTOS.COD_ANDAMENTO = 1023
    or ANDAMENTOS.COD_ANDAMENTO = 1024
    or ANDAMENTOS.COD_ANDAMENTO = 1025
    or ANDAMENTOS.COD_ANDAMENTO = 1026
    or ANDAMENTOS.COD_ANDAMENTO = 1027
    or ANDAMENTOS.COD_ANDAMENTO = 1084
    or ANDAMENTOS.COD_ANDAMENTO = 2055
    or ANDAMENTOS.COD_ANDAMENTO = 2054
    or ANDAMENTOS.COD_ANDAMENTO = 2086
    or ANDAMENTOS.COD_ANDAMENTO = 2260
    or ANDAMENTOS.COD_ANDAMENTO = 2305
    or ANDAMENTOS.COD_ANDAMENTO = 2307
    or ANDAMENTOS.COD_ANDAMENTO = 3322
    or ANDAMENTOS.COD_ANDAMENTO = 3372
    or ANDAMENTOS.COD_ANDAMENTO = 7103
    or ANDAMENTOS.COD_ANDAMENTO = 7902
    or ANDAMENTOS.COD_ANDAMENTO = 7903
    or ANDAMENTOS.COD_ANDAMENTO = 7904
    or ANDAMENTOS.COD_ANDAMENTO = 7905
    or ANDAMENTOS.COD_ANDAMENTO = 7906
    or ANDAMENTOS.COD_ANDAMENTO = 7907
    or ANDAMENTOS.COD_ANDAMENTO = 7908
    or ANDAMENTOS.COD_ANDAMENTO = 7910
-- daqui em diante estao os estranhos
    or ANDAMENTOS.COD_ANDAMENTO = 6228
    or ANDAMENTOS.COD_ANDAMENTO = 6227
    or ANDAMENTOS.COD_ANDAMENTO = 6229
    or ANDAMENTOS.COD_ANDAMENTO = 6230
    or ANDAMENTOS.COD_ANDAMENTO = 6231
)
order by PROCESSO.SEQ_OBJETO_INCIDENTE, DAT_ANDAMENTO desc
limit 10000"""
#    or ANDAMENTOS.COD_ANDAMENTO = 7909
###################################################################################################
def run():
    db = senDbConn(flagRemoteSSH=False)
    cursor = db.cursor()
    
    cursor.execute( query )
    result_tup = cursor.fetchall()
    count = 0
    last_date_for_each_proc = {}
    result_dict = {}
    count_original_entries = 0
    for tup in result_tup:
        if result_dict.get(tup[0]):
            old_end_date = result_dict[tup[0]][1] 
            new_end_date = tup[2]
            if old_end_date < new_end_date: # isto eh desnecessario pois 
                print 'swapping END DATES for case number', tup[0]
                result_dict[tup[0]] = [tup[1],tup[2]]
        else:
            result_dict[tup[0]] = [tup[1],tup[2]]
            count_original_entries += 1
        pass
    print 'original entries:',count_original_entries
#    avg = extract_avg_time(result_tup)
    avg_in_days = extract_avg_time( result_dict.values() )
    std = extract_std_dev(avg_in_days, result_dict.values())
    print avg_in_days
###################################################################################################
def extract_std_dev(avg_in_days, result_tup):
    squ = []
    for tup in result_tup:
        minus = tup[1] - tup[0]
        dist_from_avg = minus.days - avg_in_days
        squ.append(dist_from_avg * dist_from_avg)
    numerator = reduce(lambda x, y: x + y, squ)
    result = np.sqrt( (numerator / len(result_tup) ) )
    
    
    years = result // 365.25
    left = result % 365.25
    avgmonths = left // 30
    days = left % 30
    print  'STANDARD DEVIATION in days:',result
    print  'STANDARD DEVIATION have avg', years, 'years,', avgmonths, 'months, and', days, 'days'
    return result

###################################################################################################
def extract_avg_time(result_tup):
    newTest = []
    over = len(result_tup)
    totaldays = None
    totaldays2 = 0
    over365 = 0
    count = 0
    for result in result_tup:
        count += 1
       # start = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
       # end = datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S")
        minus = result[1] - result[0]
        newTest.append(minus.days)
        # minus = end - start
#        if minus.days > (365):
#            over365 += 1
#        else:
#            over365 -= 1 
        print '\t\t',count,',',minus.days
        if totaldays is None: totaldays = minus
        else: totaldays += minus
        totaldays2 += minus.days
    avgTOTALdays =  totaldays.days / over
    avgyear = avgTOTALdays // 365.25
    left = avgTOTALdays % 365.25
    avgmonth = left // 30
    avgday = left % 30
    #print 'MINUS HERE:', over365
    print  'cases have avg', avgyear, 'years,', avgmonth, 'months, and', avgday, 'days'
    print 'first avg:',avgTOTALdays
    print 'second avg:',stats.mean(newTest)
    print 'second stdDev:',stats.stdev(newTest)
    return (avgTOTALdays)
###################################################################################################
if __name__ == '__main__':
    run()
    pass