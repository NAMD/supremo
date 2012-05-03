# -*- coding:utf-8 -*-
'''
Created on Jan 30, 2012

@author: cyg
'''
from SENutils import senDbConn
from SENutils import STATE_CODES
from SENutils import write_to_csv
import os
    
###################################################################################################
CAIXA = 'Caixa Econômica Federal - CEF'
UNIAO = 'União'
PROCURADORIA_UNIAO = 'Procuradoria-Geral da União'
PROCURADORIA_FEDERAL = 'Procuradoria-Geral Federal'
INSS = 'Instituto Nacional do Seguro Social - INSS'

gdes_litigantes_normalizer = {
    'alberto cavalcante braga':CAIXA,
    'roberto maia':CAIXA,
    'helio hirasawa':CAIXA,
    'hélio hirasawa':CAIXA,
    'caixa':CAIXA,
    'Caixa Econômica Federal - CEF':CAIXA,
    'Caixa Econômica Federal':CAIXA,
    'Caixa Economica Federal':CAIXA,
    'cef':CAIXA,
    ###
    'uniao':UNIAO,
    'união':UNIAO,
    'advogado-geral da uniao':UNIAO,
    'advogado-geral da união':UNIAO,
    'advogado geral da união':UNIAO,
    'advogado geral da uniao':UNIAO,
    ###
    'Procuradoria-Geral da União':PROCURADORIA_UNIAO,
    ###
    'Procuradoria-Geral Federal':PROCURADORIA_FEDERAL,
    'Procuradoría-Geral Federal':PROCURADORIA_FEDERAL,
    ###
    'Instituto Nacional do Seguro Social - INSS':INSS
}
###################################################################################################
query = """SELECT nom_jurisdicionado, PROCEDENCIA.sig_procedencia, count(PROCESSO.num_processo)
from PROCESSO, JURISDICIONADO_INCIDENTE, PAPEL_JURISDICIONADO, JURISDICIONADO, HISTORICO_PROCESSO_ORIGEM, PROCEDENCIA
where PROCESSO.num_processo = JURISDICIONADO_INCIDENTE.num_processo
and PROCESSO.sig_classe_proces = JURISDICIONADO_INCIDENTE.sig_classe_proces
and PAPEL_JURISDICIONADO.seq_papel_jurisdicionado = JURISDICIONADO_INCIDENTE.seq_papel_jurisdicionado
and PAPEL_JURISDICIONADO.seq_jurisdicionado = JURISDICIONADO.seq_jurisdicionado
and HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente = PROCESSO.seq_objeto_incidente
and HISTORICO_PROCESSO_ORIGEM.cod_procedencia = PROCEDENCIA.cod_procedencia
and year(DAT_AUTUACAO) >= %s
and year(DAT_AUTUACAO) < %s
and PROCEDENCIA.sig_procedencia = '%s'
group by sig_procedencia, JURISDICIONADO.seq_jurisdicionado
order by count(PROCESSO.num_processo) desc, nom_jurisdicionado
limit 0 , 100
"""

START_YEAR = 2000
END_YEAR = 2011
###################################################################################################
def run():
    db = senDbConn(flagRemoteSSH=True)
    for state_code in STATE_CODES.values():
        print '\t...', state_code
        for year in range(START_YEAR,END_YEAR):
            print '\t...', year
            cursor = db.cursor()
            query_final = query % (year,year+1,str(state_code))
            print year,' - ', cursor.execute(query_final)
            resultSet = cursor.fetchall()
            dir = '../'+ str(state_code) + '/'
            if not os.path.exists(dir):
                os.makedirs(dir)
            write_to_csv('../', str(state_code) + '/' + str(year)+'.csv', ('nome da entidade','UF','quantidade'), resultSet)
            cursor.close()
#        cursor = db.cursor()
#        query_final = query % (START_YEAR,END_YEAR,str(state_code))
#        print year,' - ', cursor.execute(query_final)
#        resultSet = cursor.fetchall()    
#        write_to_csv('../', str(state_code) + '/' + str(START_YEAR)+ '_' + str(END_YEAR) + '.csv', ('nome da entidade','UF','quantidade'), resultSet)
#        cursor.close()
###################################################################################################
if __name__ == '__main__':
    run()
