select PROCESSO.seq_objeto_incidente, dat_autuacao, ANDAMENTO_PROCESSOS.dat_andamento, cod_andamento
from PROCESSO, ASSUNTO_PROCESSO, ASSUNTOS , ANDAMENTO_PROCESSOS
where (PROCESSO.sig_classe_proces = 'AP' or PROCESSO.sig_classe_proces = 'AO' )

and 
(ANDAMENTO_PROCESSOS.cod_andamento = 2054
or ANDAMENTO_PROCESSOS.cod_andamento = 8207
or ANDAMENTO_PROCESSOS.cod_andamento = 679
or ANDAMENTO_PROCESSOS.cod_andamento = 4294
or ANDAMENTO_PROCESSOS.cod_andamento = 2260
or ANDAMENTO_PROCESSOS.cod_andamento = 7103
or ANDAMENTO_PROCESSOS.cod_andamento = 2086
or ANDAMENTO_PROCESSOS.cod_andamento = 1084
or ANDAMENTO_PROCESSOS.cod_andamento = 6219
or ANDAMENTO_PROCESSOS.cod_andamento = 3372
or ANDAMENTO_PROCESSOS.cod_andamento = 3317
or ANDAMENTO_PROCESSOS.cod_andamento = 3373
or ANDAMENTO_PROCESSOS.cod_andamento = 3374
)

and PROCESSO.num_processo = ASSUNTO_PROCESSO.num_processo
and PROCESSO.sig_classe_proces = ASSUNTO_PROCESSO.sig_classe_proces


and PROCESSO.num_processo = ANDAMENTO_PROCESSOS.num_processo
and PROCESSO.sig_classe_proces = ANDAMENTO_PROCESSOS.sig_classe_proces

and ASSUNTOS.cod_assunto = ASSUNTO_PROCESSO.cod_assunto

and ASSUNTOS.dsc_assunto_completo in ( 
    select ASSUNTOS.dsc_assunto_completo from ASSUNTOS
    where ASSUNTOS.dsc_assunto_completo like 'direito penal%'
    or ASSUNTOS.dsc_assunto_completo like 'direito processual penal%'
    or ASSUNTOS.dsc_assunto_completo like 'processo penal%'
)


order by  dat_autuacao asc, dat_andamento desc
limit 300000
