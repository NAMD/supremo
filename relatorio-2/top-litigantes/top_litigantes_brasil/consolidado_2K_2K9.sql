select count(PROCESSO.seq_objeto_incidente), nom_jurisdicionado
from PROCESSO, JURISDICIONADO_INCIDENTE, PAPEL_JURISDICIONADO, JURISDICIONADO
where PROCESSO.num_processo = JURISDICIONADO_INCIDENTE.num_processo
and PROCESSO.sig_classe_proces = JURISDICIONADO_INCIDENTE.sig_classe_proces
and JURISDICIONADO_INCIDENTE.seq_papel_jurisdicionado = PAPEL_JURISDICIONADO.seq_jurisdicionado_incidente
and JURISDICIONADO.seq_jurisdicionado = PAPEL_JURISDICIONADO.seq_jurisdicionado 
and year(dat_autuacao) <= 2009
and year(dat_autuacao) >= 2000 
and PAPEL_JURISDICIONADO.seq_tipo_jurisdicionado = 1
order by count(seq_objeto_incidente) desc