#!/usr/bin/env python
# coding: utf-8

from sys import stdout
from time import strftime
from os import mkdir, path
from shutil import rmtree
from collections import Counter
from outputty import Table
from plotter import Plotter

regioes = {
           'AC': 'Norte',
           'AP': 'Norte',
           'AM': 'Norte',
           'PA': 'Norte',
           'RO': 'Norte',
           'RR': 'Norte',
           'TO': 'Norte',
           'AL': 'Nordeste',
           'BA': 'Nordeste',
           'CE': 'Nordeste',
           'MA': 'Nordeste',
           'PB': 'Nordeste',
           'PE': 'Nordeste',
           'PI': 'Nordeste',
           'RN': 'Nordeste',
           'SE': 'Nordeste',
           'GO': 'Centro-Oeste',
           'MT': 'Centro-Oeste',
           'MS': 'Centro-Oeste',
           'DF': 'Centro-Oeste',
           'ES': 'Sudeste',
           'MG': 'Sudeste',
           'RJ': 'Sudeste',
           'SP': 'Sudeste',
           'PR': 'Sul',
           'RS': 'Sul',
           'SC': 'Sul',
}

portes = {
          'SP': 'Grande',
          'RS': 'Grande',
          'RJ': 'Grande',
          'MG': 'Grande',
          'PR': 'Médio',
          'SC': 'Médio',
          'DF': 'Médio',
          'PE': 'Médio',
          'BA': 'Médio',
          'CE': 'Médio',
          'RN': 'Médio',
          'PB': 'Médio',
          'GO': 'Médio',
          'AL': 'Médio',
          'ES': 'Pequeno',
          'MS': 'Pequeno',
          'AM': 'Pequeno',
          'PA': 'Pequeno',
          'MT': 'Pequeno',
          'SE': 'Pequeno',
          'MA': 'Pequeno',
          'RO': 'Pequeno',
          'PI': 'Pequeno',
          'AC': 'Pequeno',
          'RR': 'Pequeno',
          'TO': 'Pequeno',
          'AP': 'Pequeno',
}

def log(text, date_and_time=True):
    if date_and_time:
        stdout.write('[%s] %s' % (strftime('%Y-%m-%d %H:%M:%S'), text))
    else:
        stdout.write(text)
    stdout.flush()

def deleta_e_cria_diretorio(diretorio):
    try:
        rmtree(diretorio)
    except OSError:
        pass
    mkdir(diretorio)

def gera_graficos():
    log(u'Criando gráfico de duração de processos por UF... ')
    arquivo = 'dados/duracao-processos-2000-2009.csv'
    arquivo_consolidado = 'dados-consolidados/duracao-processos-2000-2009.csv'
    t = Table()
    t.read('csv', arquivo)
    t.order_by('duracao_em_dias', 'desc')
    t['duracao_em_meses'] = [x / 30.0 for x in t['duracao_em_dias']]
    del t['duracao_em_dias']
    t.write('csv', arquivo_consolidado)
    p = Plotter(arquivo_consolidado, rows=2, cols=1)
    p.scatter(x_column='uf', title=u'Duração média de processos',
              y_label=u'Duração média (meses)', x_label='Unidade Federativa',
              legends=None, y_lim=(0, None))
    numero_de_processos = Table()
    numero_de_processos.read('csv', 'dados/processos-por-uf-2000-2009.csv')
    numero_de_processos_por_uf = {r['uf']: r['processos'] \
                                  for r in numero_de_processos.to_list_of_dicts()}
    processos_ordenados = Table(headers=numero_de_processos.headers)
    for registro in t.to_list_of_dicts():
        processos_ordenados.append((registro['uf'],
                                    numero_de_processos_por_uf[registro['uf']]))
    processos_ordenados._identify_type_of_data()
    p.data = processos_ordenados
    p.scatter(x_column='uf', title=u'',
              y_label=u'Número de processos', x_label='Unidade Federativa',
              legends=None, y_lim=(0, None))
    p.save('graficos/duracao-processos-2000-2009.png')
    log('OK\n', date_and_time=False)

    log(u'Criando gráfico de duração de processos por região... ')
    arquivo = 'dados-consolidados/duracao-processos-por-regiao-2000-2009.csv'
    titulo = u'Duração de processos por região geográfica (2000 a 2009)'
    duracao_por_regiao = Counter()
    estados_por_regiao = Counter()
    for registro in t.to_list_of_dicts():
        regiao = regioes[registro['uf']]
        duracao_por_regiao[regiao] += registro['duracao_em_meses']
        estados_por_regiao[regiao] += 1
    tabela_por_regiao = Table(headers=['regiao', 'duracao_em_meses'])
    for regiao, soma in duracao_por_regiao.iteritems():
        tabela_por_regiao.append((regiao, soma / estados_por_regiao[regiao]))
    tabela_por_regiao.order_by('duracao_em_meses', 'desc')
    tabela_por_regiao.write('csv', arquivo)
    p = Plotter(arquivo)
    p.bar(title=titulo, x_column='regiao',
          y_label=u'Duração média (meses)', legends=None)
    p.save('graficos/duracao-processos-por-regiao-2000-2009.png')
    log('OK\n', date_and_time=False)

    log(u'Criando gráfico de duração de processos por porte... ')
    arquivo = 'dados-consolidados/duracao-processos-por-porte-2000-2009.csv'
    titulo = u'Duração de processos por porte (2000 a 2009)'
    duracao_por_porte = Counter()
    estados_por_porte = Counter()
    for registro in t.to_list_of_dicts():
        porte = portes[registro['uf']]
        duracao_por_porte[porte] += registro['duracao_em_meses']
        estados_por_porte[porte] += 1
    tabela_por_porte = Table(headers=['porte', 'duracao_em_meses'])
    for porte, soma in duracao_por_porte.iteritems():
        tabela_por_porte.append((porte, soma / estados_por_porte[porte]))
    tabela_por_porte.order_by('duracao_em_meses', 'desc')
    tabela_por_porte.write('csv', arquivo)
    p = Plotter(arquivo)
    p.bar(title=titulo, x_column='porte',
          y_label=u'Duração média (meses)', legends=None)
    p.save('graficos/duracao-processos-por-porte-2000-2009.png')
    log('OK\n', date_and_time=False)

if __name__ == '__main__':
    deleta_e_cria_diretorio('graficos')
    deleta_e_cria_diretorio('dados-consolidados')
    gera_graficos()
