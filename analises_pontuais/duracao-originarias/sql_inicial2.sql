select * from ANDAMENTO_PROCESSOS, ANDAMENTOS, CLASSE
-- coneccoes de tabela
where ANDAMENTO_PROCESSOS.cod_andamento = ANDAMENTOS.cod_andamento
and ANDAMENTO_PROCESSOS.sig_classe_proces = CLASSE.SIG_CLASSE
-- somente penal
and ASSUNTO_PROCESSOS.cod_assunto in (
select cod_assunto from ASSUNTO_PROCESSOS 
where cod_assunto = 018000000 
or cod_assunto = 088000000
or cod_assunto = 1209
or cod_assunto = 188000000
or cod_assunto = 287
or,NULL,"DIREITO PENAL","DIREITO PENAL",S
)
and num_sequencia = 1
-- mato os HC
and sig_classe_proces <> 'HC'
-- codigos que ditam "ordinaria"
and ANDAMENTO_PROCESSOS.cod_andamento in (
    select cod_andamento from ANDAMENTOS where 
    ANDAMENTOS.dsc_andamento = 'AÇÃO CAUTELAR'
    or ANDAMENTOS.dsc_andamento = 'AÇÃO CÍVEL ORIGINÁRIA'
    or ANDAMENTOS.dsc_andamento = 'AÇÃO ORIGINÁRIA'
    or ANDAMENTOS.dsc_andamento = 'AÇÃO ORIGINÁRIA ESPECIAL'
    or ANDAMENTOS.dsc_andamento = 'AÇÃO PENAL'
    or ANDAMENTOS.dsc_andamento = 'AÇÃO RESCISÓRIA'
    or ANDAMENTOS.dsc_andamento = 'APELAÇÃO CÍVEL'
    or ANDAMENTOS.dsc_andamento = 'ARGÜIÇÃO DE IMPEDIMENTO'
    or ANDAMENTOS.dsc_andamento = 'ARGUIÇÃO DE RELEVÂNCIA'
    or ANDAMENTOS.dsc_andamento = 'ARGÜIÇÃO DE SUSPEIÇÃO'
    or ANDAMENTOS.dsc_andamento = 'CARTA ROGATÓRIA'
    or ANDAMENTOS.dsc_andamento = 'COMUNICAÇÃO'
    or ANDAMENTOS.dsc_andamento = 'CONFLITO DE ATRIBUIÇÕES'
    or ANDAMENTOS.dsc_andamento = 'CONFLITO DE COMPETÊNCIA'
    or ANDAMENTOS.dsc_andamento = 'CONFLITO DE JURISDIÇÃO'
    or ANDAMENTOS.dsc_andamento = 'EXCEÇÃO DA VERDADE'
    or ANDAMENTOS.dsc_andamento = 'EXCEÇÃO DE INCOMPETÊNCIA'
    or ANDAMENTOS.dsc_andamento = 'EXCEÇÃO DE LITISPENDÊNCIA'
    or ANDAMENTOS.dsc_andamento = 'EXCEÇÃO DE SUSPEIÇÃO'
    or ANDAMENTOS.dsc_andamento = 'EXTRADIÇÃO'
    or ANDAMENTOS.dsc_andamento = 'HABEAS CORPUS'
    or ANDAMENTOS.dsc_andamento = 'HABEAS DATA'
    or ANDAMENTOS.dsc_andamento = 'INQUÉRITO'
    or ANDAMENTOS.dsc_andamento = 'INTERVENÇÃO FEDERAL'
    or ANDAMENTOS.dsc_andamento = 'MANDADO DE SEGURANÇA'
    or ANDAMENTOS.dsc_andamento = 'OPOSIÇÃO EM AÇÃO CIVIL ORIGINÁRIA'
    or ANDAMENTOS.dsc_andamento = 'PETIÇÃO'
    or ANDAMENTOS.dsc_andamento = 'PETIÇÃO AVULSA'
    or ANDAMENTOS.dsc_andamento = 'PRISÃO PREVENTIVA PARA EXTRADIÇÃO'
    or ANDAMENTOS.dsc_andamento = 'PROCESSO ADMINISTRATIVO'
    or ANDAMENTOS.dsc_andamento = 'QUEIXA-CRIME'
    or ANDAMENTOS.dsc_andamento = 'RECLAMAÇÃO'
    or ANDAMENTOS.dsc_andamento = 'RECURSO CRIME'
    or ANDAMENTOS.dsc_andamento = 'RECURSO ORD. EM MANDADO DE SEGURANÇA'
    or ANDAMENTOS.dsc_andamento = 'RECURSO ORDINÁRIO EM HABEAS CORPUS'
    or ANDAMENTOS.dsc_andamento = 'RECURSO ORDINÁRIO EM HABEAS DATA'
    or ANDAMENTOS.dsc_andamento = 'RECURSO ORDINÁRIO EM MANDADO DE INJUNÇÃO'
    or ANDAMENTOS.dsc_andamento = 'REPRESENTAÇÃO'
    or ANDAMENTOS.dsc_andamento = 'REVISÃO CRIMINAL'
    or ANDAMENTOS.dsc_andamento = 'SENTENÇA ESTRANGEIRA'
    or ANDAMENTOS.dsc_andamento = 'SENTENÇA ESTRANGEIRA CONTESTADA'
    or ANDAMENTOS.dsc_andamento = 'SUSPENSÃO DE LIMINAR'
    or ANDAMENTOS.dsc_andamento = 'SUSPENSÃO DE SEGURANÇA'
    or ANDAMENTOS.dsc_andamento = 'SUSPENSÃO DE TUTELA ANTECIPADA' 
)




