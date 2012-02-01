To Do
=====


Gráficos para Segundo Relatório
-------------------------------

- [Álvaro] Processos por estado por ano / População Economicamente Ativa
- [Álvaro] Processos por estado por ano / PIB
- [Álvaro] Processos por estado por ano / PIB per capita
- [Álvaro] Processos por estado por ano / número de advogados
- Top litigantes: numero de juízes, numero de advogados, PIB, indice de
  litigiosidade do estado (pegar dados do Justiça em Números)
- Mapa político
- [OK] Por ano por estado
- [OK] Por ano por estado por porte (grande = top4, pequeno = menos de 1%,
  médio = outros)
- [OK] Gráfico de barras por tipo de corte
- [OK] Processos por categoria do Direito (em radar)


Organização de Arquivos e Diretórios
------------------------------------

- [Daniel] O que os diretórios/arquivos abaixo contém? São necessários para
  alguma de nossas análises? Se sim, colocar em um diretório que corresponda,
  senão, remover. São eles:
  - `assunto-por-estado` (relacionado a `processos-por-categoria`)
  - `classe-por-estado-por-ano` (mesmo acima)
  - `classes_por_estado` (mesmo acima)
  - `tipo_de_corte_por_classe` (relacionado a `processos-por-tipo-de-corte`)
  - `tipo_de_corte_por_estado` (mesmo acima)
  - `processos_por_data_autuacao.csv` ?
  - `top_litigantes_por_ano` ?
  - `top_litigantes_por_uf` ?
  - `top_litigantes_por_uf_ano` ?
- [Daniel] Juntar arquivo `class_mapping.py` com o que faz a query e grava os
  CSVs separados por corte e colocá-lo em `processos-por-tipo-de-corte`. Os
  arquivos que esse script salva devem ficar em
  `processos-por-tipo-de-corte/dados` (verifique o formato dos CSVs que estão
  atualmente lá para que esse formato se mantenha e os scripts de geração de
  gráficos não se quebrem).

> Nota: vamos tentar manter os nomes de arquivos separados por '-' (a não ser
> em casos de arquivos Python, senão não conseguimos usar 'import') e, sempre
> que precisarmos criar em um script um arquivo temporário (seja CSV ou
> qualquer outro), removê-lo ao final.
