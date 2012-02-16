#!/usr/bin/env python
# coding: utf-8

from plotter import Plotter
from outputty import Table
from unicodedata import normalize
from collections import Counter
import matplotlib.cm
from os import mkdir
from shutil import rmtree

def deleta_e_cria_diretorio(diretorio):
    try:
        rmtree(diretorio)
    except OSError:
        pass
    mkdir(diretorio)

deleta_e_cria_diretorio('graficos')
deleta_e_cria_diretorio('dados-consolidados')

litigantes_gerais = []
for ano in range(2000, 2010):
    p = Plotter('dados/{}.csv'.format(ano))
    dados = {uf: Counter() for uf in list(set(p.data['uf']))}
    for registro in p.data.to_list_of_dicts():
        litigante = normalize('NFKD', registro['litigante'].decode('utf8'))
        litigante = litigante.encode('ascii', 'ignore')
        dados[registro['uf']][litigante] += registro['processos']
    litigantes = []
    for uf in dados.keys():
        litigantes.extend(dados[uf].keys())
    litigantes = list(set(litigantes))
    litigantes_gerais.extend(litigantes)
litigantes_gerais = list(set(litigantes_gerais))

for ano in range(2000, 2010):
    p = Plotter('dados/%d.csv' % ano)
    dados = {uf: Counter() for uf in list(set(p.data['uf']))}
    for registro in p.data.to_list_of_dicts():
        litigante = normalize('NFKD', registro['litigante'].decode('utf8'))
        litigante = litigante.encode('ascii', 'ignore')
        dados[registro['uf']][litigante] += registro['processos']
    t = Table(headers=['uf'] + litigantes_gerais)
    for uf in dados.keys():
        row = [uf]
        for litigante in litigantes_gerais:
            if litigante in dados[uf]:
                valor = dados[uf][litigante]
            else:
                valor = 0
            row.append(valor)
        t.append(row)
    t.order_by('uf')
    others = Table()
    others.read('csv', 'dados/outros-por-uf-{}.csv'.format(ano))
    others.order_by('uf')
    t['OUTROS'] = others['processos']
    t.write('csv', 'dados-consolidados/novo-{}.csv'.format(ano))
    t = Table(headers=['uf', 'litigante', 'processos'])
    for uf in dados.keys():
        for litigante in litigantes_gerais:
            if litigante in dados[uf]:
                valor = dados[uf][litigante]
            else:
                valor = 0
            t.append([uf, litigante, valor])
    t.order_by('uf')
    t.write('csv', 'dados-consolidados/{}-organizado.csv'.format(ano))
    #p = Plotter('dados-consolidados/novo-{}.csv'.format(ano))
    #p.scatter(x_column='uf', title='Top Litigantes - Ano %d' % ano,
    #          colormap=matplotlib.cm.hsv)
    p = Plotter('dados-consolidados/{}-organizado.csv'.format(ano))
    p.stacked_bar(x_column='uf', y_column='processos', y_labels='litigante',
                  title='Top Litigantes - Ano {}'.format(ano),
                  colormap=matplotlib.cm.hsv)
    p.save('graficos/{}.png'.format(ano))
