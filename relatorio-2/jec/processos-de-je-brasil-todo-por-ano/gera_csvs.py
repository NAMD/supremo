'''
Created on Apr 3, 2012

@author: cyg
'''
from SENutils import senDbConn
from SENutils import write_to_csv
###################################################################################################
query_desagregando_por_juizado = """select dsc_origem as 'Origem', count(PROCESSO.seq_objeto_incidente) as 'Processos' 
from ORIGEM, HISTORICO_PROCESSO_ORIGEM, PROCESSO
where HISTORICO_PROCESSO_ORIGEM.cod_origem = ORIGEM.cod_origem
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
where HISTORICO_PROCESSO_ORIGEM.cod_origem = ORIGEM.cod_origem
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
    
    query_pronta = query % (str(START_YEAR), str(END_YEAR))
    cursor.execute(query_pronta)
    result_tup = cursor.fetchall()
    write_to_csv('dados/', 'consolidado.csv', ('Ano','Processos'), result_tup)
#    for year in range(START_YEAR,END_YEAR+1):
#        query_ano = query % (str(year), str(year))
#        cursor.execute(query_ano)
#        result_ano = cursor.fetchall()
#        write_to_csv('dados/', str(year)+'.csv', ('Origem','Processos'), result_ano)
    cursor.close()
    pass
###################################################################################################
if __name__ == '__main__':
    run()
    pass