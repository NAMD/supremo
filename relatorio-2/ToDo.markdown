To Do
=====

Por Estado
----------

- JEC
- Por Categoria
- Por UF por ano


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
  - `top_litigantes_por_uf` ?
  - `top_litigantes_por_uf_ano` ?
- [Daniel] Juntar arquivo `class_mapping.py` com o que faz a query e grava os
  CSVs separados por corte e colocá-lo em `processos-por-tipo-de-corte`. Os
  arquivos que esse script salva devem ficar em
  `processos-por-tipo-de-corte/dados` (verifique o formato dos CSVs que estão
  atualmente lá para que esse formato se mantenha e os scripts de geração de
  gráficos não se quebrem).
- [Daniel] Adicionar `gerar_csvs.py` em `processos-por-categoria`
- [Daniel] Rever query do `processos-por-categoria`, pois o somatório de
  processos está dando 1.7M+ (um processo pode estar em mais de uma categoria?
  Se sim, somar isso tudo para ver se dá 1.7M+).

> Nota: vamos tentar manter os nomes de arquivos separados por '-' (a não ser
> em casos de arquivos Python, senão não conseguimos usar 'import') e, sempre
> que precisarmos criar em um script um arquivo temporário (seja CSV ou
> qualquer outro), removê-lo ao final.
