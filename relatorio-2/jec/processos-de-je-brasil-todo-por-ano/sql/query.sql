select dsc_origem as 'origem', count(PROCESSO.seq_objeto_incidente) as 'num de processos' 
from ORIGEM, HISTORICO_PROCESSO_ORIGEM, PROCESSO
where HISTORICO_PROCESSO_ORIGEM.cod_origem = ORIGEM.cod_origem
and PROCESSO.seq_objeto_incidente = HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente
and (dsc_origem like '%esp.%' OR dsc_origem like '%espec%' OR dsc_origem like '%peq%')
and dsc_origem not like '%especializad%'
and ORIGEM.cod_origem <> 1277
and ORIGEM.cod_origem <> 1521
and year(dat_autuacao) >= 2000
and year(dat_autuacao) <= 2009
group by dsc_origem
order by count(PROCESSO.seq_objeto_incidente) desc