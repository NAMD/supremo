select PROCESSO.seq_objeto_incidente,PROCESSO.num_processo, PROCESSO.sig_classe_proces, ANDAMENTO_PROCESSOS.num_sequencia, PROCESSO.dat_autuacao, ANDAMENTO_PROCESSOS.dat_andamento, ANDAMENTOS.dsc_andamento
from PROCESSO, ANDAMENTOS, ANDAMENTO_PROCESSOS, HISTORICO_PROCESSO_ORIGEM
where PROCESSO.num_processo = ANDAMENTO_PROCESSOS.num_processo
and PROCESSO.sig_classe_proces = ANDAMENTO_PROCESSOS.sig_classe_proces
and ANDAMENTO_PROCESSOS.cod_andamento = ANDAMENTOS.cod_andamento
and HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente = PROCESSO.seq_objeto_incidente
and HISTORICO_PROCESSO_ORIGEM.cod_procedencia = 7
and ANDAMENTOS.DSC_ANDAMENTO in
(
    select DSC_ANDAMENTO from ANDAMENTOS where DSC_ANDAMENTO like '%publica%'
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
order by num_processo,PROCESSO.sig_classe_proces desc
limit 100000