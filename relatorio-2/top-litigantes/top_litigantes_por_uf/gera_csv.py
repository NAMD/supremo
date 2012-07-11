'''
Created on May 9, 2012

@author: cyg
'''
from SENutils import senDbConn
from SENutils import write_to_csv
import time

query = """select nom_jurisdicionado, count(PROCESSO.seq_objeto_incidente)
from PAPEL_JURISDICIONADO,  JURISDICIONADO, JURISDICIONADO_INCIDENTE, PROCESSO, HISTORICO_PROCESSO_ORIGEM, OBJETO_INCIDENTE
where PAPEL_JURISDICIONADO.seq_jurisdicionado = JURISDICIONADO.seq_jurisdicionado
and JURISDICIONADO_INCIDENTE.seq_papel_jurisdicionado = PAPEL_JURISDICIONADO.seq_papel_jurisdicionado
and PROCESSO.num_processo = JURISDICIONADO_INCIDENTE.num_processo
and PROCESSO.sig_classe_proces = JURISDICIONADO_INCIDENTE.sig_classe_proces
and PROCESSO.seq_objeto_incidente = HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente
and year(PROCESSO.dat_autuacao) = 2000
and PAPEL_JURISDICIONADO.seq_tipo_jurisdicionado = 1
and HISTORICO_PROCESSO_ORIGEM.cod_procedencia = 7
group by nom_jurisdicionado
order by count(PROCESSO.seq_objeto_incidente) desc
"""

#query = "select * from PROCESSO limit 10"
if __name__ == '__main__':
    print 'starting'
    a = int(round(time.time() * 1000))
    
    start = int(round(time.time() * 1000))
    conn = senDbConn(flagManual=True, host='10.250.49.180', port=3306, user='root', passwd='mysqlFGV13', db='STF_O')
    cursor = conn.cursor()
    b = int(round(time.time() * 1000))
    print b-a, 'executing'
    
    cursor.execute(query)
    c = int(round(time.time() * 1000))
    print c-a, 'done with execute, entering fetchall'
    
    all = cursor.fetchall()
    d = int(round(time.time() * 1000))
    print d-a, 'left fetchall, entering write_to_csv'
    
    write_to_csv("testest/", "dude.csv", ("nome","processos"), all)
    e = int(round(time.time() * 1000))
    print e-a, 'done'
