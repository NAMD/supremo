#!/usr/bin/env python
# coding: utf-8

from os import mkdir, remove, path
from shutil import rmtree
from glob import glob
from outputty import Table
from gera_graficos import plota_graficos, log


try:
    rmtree('graficos')
except OSError:
    pass
mkdir('graficos')

log('Calculando o número total de processos... ')
dados = {}
conteudo = []
for arquivo in sorted(glob('dados/processos-por-uf-????.csv')):
    t = Table()
    t.read('csv', arquivo)
    for registro in t.to_list_of_dicts():
        dados[registro['uf']] = registro['processos']
    conteudo.append((arquivo, t[:]))
tabela_geral = Table(headers=['uf', 'processos'])
for uf, processos in dados.iteritems():
    tabela_geral.append((uf, processos))
tabela_geral.order_by('processos', 'desc')
total_de_processos = float(sum(tabela_geral['processos']))

log('OK\n', date_and_time=False)
log('Definindo portes das UFs... ')
grande_porte = [registro[0] for registro in tabela_geral[:4]]
del tabela_geral[:4]
for indice, registro in enumerate(tabela_geral.to_list_of_dicts()):
    if registro['processos'] / total_de_processos <= 0.01:
        break
pequeno_porte = [registro[0] for registro in tabela_geral[indice:]]
del tabela_geral[indice:]
medio_porte = [registro[0] for registro in tabela_geral]
del tabela_geral

log('OK\n', date_and_time=False)
log('Separando portes por ano e gerando gráficos...\n')
for arquivo, registros in conteudo:
    ano = arquivo.replace('dados/processos-por-uf-', '').replace('.csv', '')
    log('  {}: '.format(ano))
    t = Table(headers=['uf', 'processos'])
    t.extend(registros)
    total_de_processos = sum(t['processos'])
    tabela_grande_porte = Table(headers=t.headers)
    tabela_medio_porte = Table(headers=t.headers)
    tabela_pequeno_porte = Table(headers=t.headers)
    for registro in t.to_list_of_dicts():
        if registro['uf'] in grande_porte:
            tabela_grande_porte.append(registro)
        elif registro['uf'] in medio_porte:
            tabela_medio_porte.append(registro)
        elif registro['uf'] in pequeno_porte:
            tabela_pequeno_porte.append(registro)
    tabela_pequeno_porte.order_by('processos', 'desc')
    tabela_medio_porte.order_by('processos', 'desc')
    tabela_grande_porte.order_by('processos', 'desc')
    p = 'dados/tmp-pequeno-porte-{}.csv'.format(ano)
    m = 'dados/tmp-medio-porte-{}.csv'.format(ano)
    g = 'dados/tmp-grande-porte-{}.csv'.format(ano)
    tabela_pequeno_porte.write('csv', p)
    tabela_medio_porte.write('csv', m)
    tabela_grande_porte.write('csv', g)
    plota_graficos(p, 'graficos/' + path.basename(p.replace('.csv', '.png')),
                   'Processos de {} - Pequeno Porte'.format(ano),
                   y_lim=(0, 15000), total_de_processos=total_de_processos,
                   y_lim_bar=(0, 3.5), titulo_bar='Percentual no ano')
    plota_graficos(m, 'graficos/' + path.basename(m.replace('.csv', '.png')),
                   u'Processos de {} - Médio Porte'.format(ano),
                   y_lim=(0, 120000), total_de_processos=total_de_processos,
                   y_lim_bar=(0, 12), titulo_bar='Percentual no ano')
    plota_graficos(g, 'graficos/' + path.basename(g.replace('.csv', '.png')),
                   'Processos de {} - Grande Porte'.format(ano),
                   y_lim=(0, 155000), total_de_processos=total_de_processos,
                   y_lim_bar=(0, 25), titulo_bar='Percentual no ano')
    remove(p)
    remove(m)
    remove(g)
    log('OK\n', date_and_time=False)
log('Done!\n')
