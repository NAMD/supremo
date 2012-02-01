'''
Created on Feb 1, 2012

@author: cyg
'''
from SENutils import senDbConn
from SENutils import write_to_csv
###############################################################################    
query = """ select PROCEDENCIA.sig_procedencia as UF, count(distinct PROCESSO.SEQ_OBJETO_INCIDENTE) as qtde
from PROCESSO, JURISDICIONADO_INCIDENTE, PAPEL_JURISDICIONADO, JURISDICIONADO, HISTORICO_PROCESSO_ORIGEM, PROCEDENCIA
where PROCESSO.num_processo = JURISDICIONADO_INCIDENTE.num_processo
and PROCESSO.sig_classe_proces = JURISDICIONADO_INCIDENTE.sig_classe_proces
and PAPEL_JURISDICIONADO.seq_papel_jurisdicionado = JURISDICIONADO_INCIDENTE.seq_papel_jurisdicionado
and PAPEL_JURISDICIONADO.seq_jurisdicionado = JURISDICIONADO.seq_jurisdicionado
and HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente = PROCESSO.seq_objeto_incidente
and HISTORICO_PROCESSO_ORIGEM.cod_procedencia = PROCEDENCIA.cod_procedencia
and year(DAT_AUTUACAO) >= %s
and year(DAT_AUTUACAO) < %s
and sig_procedencia <> '**'
and sig_procedencia <> '***'
and sig_procedencia <> 'UF'
group by sig_procedencia, year(DAT_AUTUACAO)
order by sig_procedencia, year(DAT_AUTUACAO)
limit 0 , 300000 """

START_YEAR = 2000
END_YEAR = 2012
###############################################################################    
def run():
    conn = senDbConn(flagRemoteSSH=True)
    cursor = conn.cursor()
    for year in range(START_YEAR,END_YEAR):
        query_pronta = query % ( str(year), str(year+1) )
        cursor.execute(query_pronta)
        resultSet = cursor.fetchall()
        write_to_csv("dados/", str(year)+".csv", ('uf','processos'), resultSet)
        print year, '...'
###############################################################################    
if __name__ == '__main__':
    run()