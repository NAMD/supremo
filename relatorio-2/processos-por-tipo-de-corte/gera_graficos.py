#!/usr/bin/env python
# coding: utf-8

from os import remove, mkdir
from shutil import rmtree
from glob import glob
from time import strftime
from outputty import Table
from plotter import Plotter


def log(text):
    print('[{}] {}'.format(strftime('%Y-%m-%d %H:%M:%S'), text))

try:
    rmtree('graficos')
except OSError:
    pass
mkdir('graficos')

log('Normalizando dados...')
table = Table(headers=['UF', u'Ordinária', 'Constitucional',
                       'Recursal de Massa', 'Total'])
for arquivo in glob('dados/*.csv'):
    uf = arquivo.replace('.csv', '')
    t = Table()
    t.read('csv', arquivo)
    data = {'UF': uf, 'Total': 0}
    for registro in t.to_list_of_dicts(encoding=None):
        data[registro['corte']] = registro['processos']
        data['Total'] += registro['processos']
    table.append(data)
table.order_by('Total', 'desc')
del table['Total']
table.write('csv', 'dados/tmp-processos-por-tipo-de-corte.csv')

log('Plotando gráficos...')
p = Plotter('dados/tmp-processos-por-tipo-de-corte.csv', width=1600,
            height=1200, rows=4, cols=1)
p.bar(x_column='UF', title=u'Processos - Recursal de Massa (todos os anos)',
      bar_width=0.5, y_columns=['Recursal de Massa'], colors=['r'])
p.bar(x_column='UF', title=u'Processos - Ordinária (todos os anos)',
      bar_width=0.5, y_columns=[u'Ordinária'], colors=['g'])
p.bar(x_column='UF', title=u'Processos - Constitucional (todos os anos)',
      bar_width=0.5, y_columns=['Constitucional'], colors=['b'])
p.bar(x_column='UF', title=u'Processos - todas as cortes (todos os anos)',
      bar_width=0.5,
      y_columns=['Recursal de Massa', u'Ordinária', 'Constitucional'],
      colors=['r', 'g', 'b'])
p.save('graficos/processos-por-tipo-de-corte.png')
remove('dados/tmp-processos-por-tipo-de-corte.csv')
log('Done!')
