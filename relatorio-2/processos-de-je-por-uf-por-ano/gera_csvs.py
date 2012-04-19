'''
Created on Mar 14, 2012

@author: cyg
'''
from SENutils import senDbConn
from SENutils import write_to_csv
from SENutils import STATE_KEYS
###################################################################################################
query_desagregando_por_juizado = """select dsc_origem as 'origem', count(PROCESSO.seq_objeto_incidente) as 'num de processos' 
from ORIGEM, HISTORICO_PROCESSO_ORIGEM, PROCESSO
where HISTORICO_PROCESSO_ORIGEM.cod_procedencia = %s
and HISTORICO_PROCESSO_ORIGEM.cod_origem = ORIGEM.cod_origem
and PROCESSO.seq_objeto_incidente = HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente
and (dsc_origem like '%%esp.%%' OR dsc_origem like '%%espec%%' OR dsc_origem like '%%peq%%')
and dsc_origem not like '%%especializad%%'
and ORIGEM.cod_origem <> 1277
and ORIGEM.cod_origem <> 1521
and year(dat_autuacao) >= %s
and year(dat_autuacao) <= %s
group by dsc_origem
order by count(PROCESSO.seq_objeto_incidente) desc
"""
###################################################################################################
query = """select year(dat_autuacao) as 'Ano', count(PROCESSO.seq_objeto_incidente) as 'Processos' 
from ORIGEM, HISTORICO_PROCESSO_ORIGEM, PROCESSO
where HISTORICO_PROCESSO_ORIGEM.cod_procedencia = %s
and HISTORICO_PROCESSO_ORIGEM.cod_origem = ORIGEM.cod_origem
and PROCESSO.seq_objeto_incidente = HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente
and (dsc_origem like '%%esp.%%' OR dsc_origem like '%%espec%%' OR dsc_origem like '%%peq%%')
and dsc_origem not like '%%especializad%%'
and ORIGEM.cod_origem <> 1277
and ORIGEM.cod_origem <> 1521
and year(dat_autuacao) >= %s
and year(dat_autuacao) <= %s
group by year(dat_autuacao)
order by year(dat_autuacao)
"""
START_YEAR = 2000
END_YEAR = 2009
###################################################################################################
def run():  
    db = senDbConn()
    cursor = db.cursor()
    
    for state in STATE_KEYS.items():
        query_pronta = query % (state[1], str(START_YEAR), str(END_YEAR))
        cursor.execute(query_pronta)
        result_tup = cursor.fetchall()
        result_list = list(result_tup)
        # making sure all years are filled out, those that don't appear will be inserted as having 0 
        years = range(START_YEAR, END_YEAR+1)
        counter = 0
        for item in result_list:
            if item[0] != years[counter]:
                result_list.insert(counter, (long(years[counter]), long(0)) )
            counter+=1
        write_to_csv('dados/', state[0]+'.csv', ('Ano','Processos'), result_tup)
#        for year in range(START_YEAR,END_YEAR+1):
#            print year
#            query_ano = query % (state[1], str(year), str(year))
#            cursor.execute(query_ano)
#            result_ano = cursor.fetchall()
#            write_to_csv('dados/'+state[0]+'/', str(year)+'.csv', ('Origem','Num. de Processos'), result_ano)
        print state[0], 'done'
    cursor.close()      
###################################################################################################
if __name__ == '__main__':
    run()
