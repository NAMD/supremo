select distinct PROCESSO.seq_objeto_incidente,  PROCEDENCIA.sig_procedencia, year(PROCESSO.dat_autuacao)
from PROCESSO, OBJETO_INCIDENTE, HISTORICO_PROCESSO_ORIGEM, PROCEDENCIA
where PROCESSO.seq_objeto_incidente = OBJETO_INCIDENTE.seq_objeto_incidente
AND OBJETO_INCIDENTE.seq_objeto_incidente = HISTORICO_PROCESSO_ORIGEM.seq_objeto_incidente
AND HISTORICO_PROCESSO_ORIGEM.cod_procedencia = PROCEDENCIA.cod_procedencia
limit 1500000