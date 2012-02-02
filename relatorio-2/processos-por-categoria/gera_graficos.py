#!/usr/bin/env python
# coding: utf-8

from os import mkdir, remove
from shutil import rmtree
from time import strftime
from glob import glob
from collections import Counter
from outputty import Table
from plotter import Plotter


def log(text):
    print('[{}] {}'.format(strftime('%Y-%m-%d %H:%M:%S'), text))

try:
    rmtree('graficos')
except OSError:
    pass
mkdir('graficos')

log('Normalizando estrutura...')
areas = []
for arquivo in glob('dados/*.csv'):
    table = Table()
    table.read('csv', arquivo)
    coluna = 'area'
    if 'COLUNA A' in table.headers:
        coluna = 'COLUNA A'
    areas.extend(table[coluna])

areas = set(areas)
for arquivo in sorted(glob('dados/*.csv')):
    table = Table()
    table.read('csv', arquivo)
    if 'COLUNA A' in table.headers:
        table['area'] = table['COLUNA A']
        table['processos'] = table['COLUNA B']
        del table['COLUNA A']
        del table['COLUNA B']
    for nova_area in list(areas - set(table['area'])):
        table.append({'area': nova_area, 'processos': 0})
    for registro in table:
        registro[0] = registro[0].capitalize()
        registro[0] = registro[0].replace('Direito ', '').capitalize()
        registro[0] = registro[0].replace(
                u'Administrativo e outras matérias de direito público',
                u'Administrativo/Público (outras)')
    table.write('csv', arquivo)

consolidado = Counter()
log('Plotando...')
for arquivo in sorted(glob('dados/*.csv')):
    estado = arquivo.split('-')[-1].replace('.csv', '')
    log('  {}'.format(estado))
    p = Plotter(arquivo, width=1400, height=1050)
    for registro in p.data.to_list_of_dicts():
        consolidado[registro['area']] += registro['processos']
    p.data['Legenda'] = [u'Número de processos' for x in p.data]
    p.radar(axis_labels='area', values='processos',
            legends_column='Legenda', legends=False,
            title=u'Processos por Área - ' + estado)
    p.save('graficos/processos-por-categoria-{}.png'.format(estado))

log('Plotando gráfico consolidado...')
tabela_geral = Table(headers=['area', 'processos'])
for item in consolidado.iteritems():
    tabela_geral.append(item)
tabela_geral.write('csv', 'dados/tmp-consolidado.csv')
p = Plotter('dados/tmp-consolidado.csv', width=1400, height=1050)
p.data['Legenda'] = [u'Número de processos' for x in p.data]
p.radar(axis_labels='area', values='processos', legends_column='Legenda',
        legends=False, title=u'Processos por Área - Brasil')
p.save('graficos/processos-por-categoria-brasil.png')
remove('dados/tmp-consolidado.csv')
log('Done!')
