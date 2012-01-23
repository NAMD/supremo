#!/usr/bin/env python
# coding: utf-8

from time import strftime
from glob import glob
from outputty import Table
from plotter import Plotter


def log(text):
    print('[{}] {}'.format(strftime('%Y-%m-%d %H:%M:%S'), text))

log('Normalizing structure...')
areas = []
for arquivo in glob('*.csv'):
    table = Table()
    table.read('csv', arquivo)
    coluna = 'area'
    if 'COLUNA A' in table.headers:
        coluna = 'COLUNA A'
    areas.extend(table[coluna])

areas = set(areas)
for arquivo in glob('*.csv'):
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

log('Plotting data...')
for arquivo in glob('*.csv'):
    estado = arquivo.split('-')[-1].replace('.csv', '')
    p = Plotter(arquivo, width=1400, height=1050)
    p.data['Legenda'] = [u'Número de processos' for x in p.data]
    p.radar(axis_labels='area', values='processos',
            legends_column='Legenda', legends=False,
            title=u'Processos por Área - ' + estado)
    p.save('processos-por-categoria-{}.png'.format(estado))
log('Done!')
