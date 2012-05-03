# -*- coding:utf-8 -*-
'''
Created on Jan 17, 2012

@author: cyg
'''
from statlib import stats
from SENutils import load_csv
from SENutils import write_to_csv
from SENutils import senDbConn


descriptives_by_rootsubject = {}
###############################################################################
def blah(item):
    return item[1]
# sortedItems = sorted(bystateitems.items(), key=blah  )[::-1]
###############################################################################
def getrootsubjects():
    conn = senDbConn()
    cursor = conn.cursor()
    query = "SELECT DSC_ASSUNTO_COMPLETO from ASSUNTOS where COD_ASSUNTO_PAI is NULL"
    cursor.execute(query)
    result_tup = cursor.fetchall()
    cursor.close()
    return result_tup
###############################################################################
def run():
    
    rootsubjects = getrootsubjects()
    
    # cuidado: pode haver um processo com dois andamentos que cabem nos filtros
    # passados, assim é importante filtrar os resultados desta query para manter
    # somente o (cronologicamente) último andamento
    startswithquery = """SELECT PROCESSO.seq_objeto_incidente
        , ASSUNTOS.DSC_ASSUNTO_COMPLETO, PROCESSO.DAT_AUTUACAO
        , ANDAMENTO_PROCESSOS.DAT_ANDAMENTO, FLG_ULTIMO_ANDAMENTO
        FROM PROCESSO, ASSUNTOS, ASSUNTO_PROCESSO, ANDAMENTOS, ANDAMENTO_PROCESSOS
        WHERE PROCESSO.num_processo = ASSUNTO_PROCESSO.num_processo
        AND PROCESSO.sig_classe_proces = ASSUNTO_PROCESSO.sig_classe_proces
        AND ASSUNTOS.cod_assunto = ASSUNTO_PROCESSO.cod_assunto
        AND ASSUNTOS.DSC_ASSUNTO_COMPLETO like '%s%%'
        AND PROCESSO.num_processo = ANDAMENTO_PROCESSOS.num_processo
        and PROCESSO.sig_classe_proces = ANDAMENTO_PROCESSOS.sig_classe_proces
        and ANDAMENTO_PROCESSOS.cod_andamento = ANDAMENTOS.cod_andamento
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
        order by PROCESSO.SEQ_OBJETO_INCIDENTE, DAT_ANDAMENTO desc
    """
    dat_autuacao_idx = 2
    dat_fechamento_idx = 3
    conn = senDbConn()
    cursor = conn.cursor()
    total_cases_processed = 0
    for rootsubject in rootsubjects: 
        readyquery = startswithquery % rootsubject
        cursor.execute(readyquery)
        count_original_entries = 0
        clean_result_dict = {} # ==> {num_processo: [startDate,endDate]}
        cases_per_subjectOfASameRoot_tup = cursor.fetchall() # aqui tenho uma lista enorme de processos para o assunto
        for tup in cases_per_subjectOfASameRoot_tup:
            old_end_date = None
            #for legibility:
            id_case = tup[0]
            start_date = tup[2]
            end_date = tup[3]
            #############
            # make sure there will be no repeated cases considered and that 
            # the longest start/end date is chosen for each case
            #############
            if clean_result_dict.get(id_case):
                old_end_date = clean_result_dict[id_case][1] 
                new_end_date = end_date
                if old_end_date and old_end_date < new_end_date: # isto eh desnecessario pois 
                    print 'NEED TO swapping END DATES for case number', tup[0]
                    #clean_result_dict[tup[0]] = [tup[1],tup[2]]
            else:
                clean_result_dict[id_case] = [start_date,end_date]
                count_original_entries += 1
        
            
        total_cases_processed += len(cases_per_subjectOfASameRoot_tup)
        print 'original result length:',rootsubject,len(cases_per_subjectOfASameRoot_tup)
        print 'clean results length', len(clean_result_dict.keys())
        if not len(clean_result_dict.keys()):
            continue
        xx = extract_avg_time(clean_result_dict.values(), 0, 1, rootsubject[0])
        print 'AVG_DURATION_EXTRACTED:', xx
        print '==================================================================='
    print 'total_cases_processed:',total_cases_processed
    pass
    cursor.close()
    ###########################################################################
def extract_avg_time(result_tup, start_date_idx, end_date_idx, name_of_class):
    over = len(result_tup)
    totaldays = None

    for result in result_tup:

       # start = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
       # end = datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S")
        minus = result[end_date_idx] - result[start_date_idx]
        # minus = end - start
        if totaldays is None: totaldays = minus
        else: totaldays += minus
    
    #####
    avgTOTALdays =  totaldays.days / over
    avgyear = avgTOTALdays // 365.25
    left = avgTOTALdays % 365.25
    avgmonth = left // 30
    avgday = left % 30
    #####
    
    print name_of_class, 'has avg', avgyear, 'years,', avgmonth, 'months, and', avgday, 'days'
    return (avgTOTALdays)
###############################################################################
if __name__ == '__main__':
    run()