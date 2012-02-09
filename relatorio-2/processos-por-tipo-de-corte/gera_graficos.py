#!/usr/bin/env python
# coding: utf-8

from os import mkdir, path
from shutil import rmtree
from glob import glob
from time import strftime
from outputty import Table
from plotter import Plotter


def log(text):
    print('[{}] {}'.format(strftime('%Y-%m-%d %H:%M:%S'), text))

def deleta_e_cria_diretorio(diretorio):
    try:
        rmtree(diretorio)
    except OSError:
        pass
    mkdir(diretorio)

deleta_e_cria_diretorio('graficos')
deleta_e_cria_diretorio('dados-consolidados')

log('Normalizando dados...')
table = Table(headers=['UF', u'Ordinária', 'Constitucional',
                       'Recursal de Massa', 'Total'])
for arquivo in glob('dados/*.csv'):
    uf = path.basename(arquivo).replace('.csv', '')
    t = Table()
    t.read('csv', arquivo)
    data = {'UF': uf, 'Total': 0}
    for registro in t.to_list_of_dicts(encoding=None):
        data[registro['corte']] = registro['processos']
        data['Total'] += registro['processos']
    table.append(data)
table.order_by('Total', 'desc')
del table['Total']
arquivo = 'dados-consolidados/processos-por-tipo-de-corte.csv'
table.write('csv', arquivo)

log('Plotando gráficos...')
p = Plotter(arquivo, width=1600,
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
log('Done!')
