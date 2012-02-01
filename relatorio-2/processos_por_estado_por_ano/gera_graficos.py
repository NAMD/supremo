#!/usr/bin/env python
# coding: utf-8

from sys import stdout
from time import strftime
from os import mkdir, remove
from shutil import rmtree
from glob import glob
from collections import Counter
from outputty import Table
from plotter import Plotter


def log(text, date_and_time=True):
    if date_and_time:
        stdout.write('[%s] %s' % (strftime('%Y-%m-%d %H:%M:%S'), text))
    else:
        stdout.write(text)
    stdout.flush()

def plota_graficos(arquivo, imagem, titulo, y_lim=(0, 160000)):
    p = Plotter(arquivo, rows=3, cols=1)
    p.scatter(x_column='uf', title=titulo,
              order_by='uf', ordering='asc', labels=False, legends=None,
              y_lim=y_lim)
    p.scatter(x_column='uf', title='', order_by='processos', ordering='desc',
              labels=False, legends=None, y_lim=y_lim)
    total_processos = float(sum(p.data['processos']))
    p.data['processos'] = [100 * x / total_processos for x in p.data['processos']]
    p.data.order_by('processos', 'desc')
    p.bar(x_column='uf', title='', legends=None,
          y_label='Percentual de processos', y_lim=(0, 30))
    p.save(imagem)


if __name__ == '__main__':
    try:
        rmtree('graficos')
    except OSError:
        pass
    mkdir('graficos')

    log('Criando gráficos por ano... ')
    tabelas = []
    anos = []
    for arquivo in glob('processos-por-uf-????.csv'):
        ano = arquivo.split('-')[-1].split('.')[0]
        anos.append(int(ano))
        p = plota_graficos(arquivo,
                           'graficos/' + arquivo.replace('.csv', '.png'),
                           'Processos por UF de ' + ano)
        tabela = Table()
        tabela.read('csv', arquivo)
        tabelas.append(tabela)
    log('OK\n', date_and_time=False)
    log('Criando gráfico consolidado... ')
    processos = Counter()
    for tabela in tabelas:
        for registro in tabela.to_list_of_dicts():
            processos[registro['uf']] += registro['processos']
    tabela = Table(headers=['uf', 'processos'])
    for item in processos.iteritems():
        tabela.append(item)
    tabela.write('csv', 'processos-por-uf-geral.csv')
    plota_graficos('processos-por-uf-geral.csv',
                   'graficos/processos-por-estado-2000-a-2010.png',
                   'Processos por UF de {} a {}'.format(min(anos), max(anos)),
                   y_lim=(0, 1000000))
    remove('processos-por-uf-geral.csv')
    log('OK\n', date_and_time=False)
    log('Done!\n')
