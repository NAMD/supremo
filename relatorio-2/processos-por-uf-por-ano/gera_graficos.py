#!/usr/bin/env python
# coding: utf-8

from sys import stdout
from time import strftime
from os import mkdir, remove, path
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

def plota_graficos(arquivo, imagem, titulo, total_de_processos,
                   y_lim=(0, 160000), y_lim_bar=(0, 30), titulo_2='',
                   titulo_bar=''):
    p = Plotter(arquivo, rows=3, cols=1)
    p.scatter(x_column='uf', title=titulo,
              order_by='uf', ordering='asc', labels=False, legends=None,
              y_lim=y_lim)
    p.scatter(x_column='uf', title=titulo_2, order_by='processos', ordering='desc',
              labels=False, legends=None, y_lim=y_lim)
    p.data['processos'] = [100.0 * x / total_de_processos \
                           for x in p.data['processos']]
    p.data.order_by('processos', 'desc')
    p.bar(x_column='uf', title=titulo_bar, legends=None,
          y_label='Percentual de processos', y_lim=y_lim_bar)
    p.save(imagem)

def gera_graficos_por_ano():
    log('Criando gráficos por ano... ')
    tabelas = []
    anos = []
    for arquivo in glob('dados/processos-por-uf-????.csv'):
        t = Table()
        t.read('csv', arquivo)
        ano = arquivo.split('-')[-1].split('.')[0]
        anos.append(int(ano))
        imagem = 'graficos/' + path.basename(arquivo.replace('.csv', '.png'))
        p = plota_graficos(arquivo, imagem,
                           'Processos por UF de ' + ano,
                           total_de_processos=sum(t['processos']))
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
    tabela.write('csv', 'dados/tmp-processos-por-uf-geral.csv')
    plota_graficos('dados/tmp-processos-por-uf-geral.csv',
                   'graficos/processos-por-estado-2000-a-2010.png',
                   'Processos por UF de {} a {}'.format(min(anos), max(anos)),
                   y_lim=(0, 1000000),
                   total_de_processos=sum(tabela['processos']))
    remove('dados/tmp-processos-por-uf-geral.csv')
    log('OK\n', date_and_time=False)
    log('Done!\n')

def gera_graficos_por_porte():
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
                       y_lim=(0, 4000), total_de_processos=total_de_processos,
                       y_lim_bar=(0, 3.5), titulo_bar='Percentual no ano')
        plota_graficos(m, 'graficos/' + path.basename(m.replace('.csv', '.png')),
                       u'Processos de {} - Médio Porte'.format(ano),
                       y_lim=(0, 12000), total_de_processos=total_de_processos,
                       y_lim_bar=(0, 12), titulo_bar='Percentual no ano')
        plota_graficos(g, 'graficos/' + path.basename(g.replace('.csv', '.png')),
                       'Processos de {} - Grande Porte'.format(ano),
                       y_lim=(0, 30000), total_de_processos=total_de_processos,
                       y_lim_bar=(0, 25), titulo_bar='Percentual no ano')
        remove(p)
        remove(m)
        remove(g)
        log('OK\n', date_and_time=False)
    log('Done!\n')


if __name__ == '__main__':
    try:
        rmtree('graficos')
    except OSError:
        pass
    mkdir('graficos')

    gera_graficos_por_ano()
    gera_graficos_por_porte()
