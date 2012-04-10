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

def log(text, date_and_time=True):
    if date_and_time:
        stdout.write('[%s] %s' % (strftime('%Y-%m-%d %H:%M:%S'), text))
    else:
        stdout.write(text)
    stdout.flush()

def dict_to_csv(data, headers, filename, order_by=None, ordering='asc'):
    table = Table(headers=headers)
    table.extend(data.items())
    if order_by is not None:
        table.order_by(order_by, ordering)
    table.write('csv', filename)

def gera_graficos():
    log('Criando gráfico consolidado por UF... ')
    arquivo = 'dados/processos-juizados-especiais-por-uf-por-ano.csv'
    arquivo_consolidado_uf = \
            'dados-consolidados/processos-juizados-especiais-por-uf.csv'
    arquivo_consolidado_regiao = \
            'dados-consolidados/processos-juizados-especiais-por-regiao.csv'
    arquivo_consolidado_ano = \
            'dados-consolidados/processos-juizados-especiais-por-ano.csv'
    consolidado_uf = Counter()
    consolidado_uf_ano = {}
    consolidado_regiao = Counter()
    consolidado_regiao_ano = {}
    tabela = Table()
    tabela.read('csv', arquivo)
    anos = set(tabela['ano'])
    for registro in tabela.to_list_of_dicts():
        uf = registro['uf']
        regiao = regioes[uf]
        processos = registro['processos']
        ano = registro['ano']
        consolidado_uf[uf] += processos
        consolidado_regiao[regiao] += processos
        if uf not in consolidado_uf_ano:
            consolidado_uf_ano[uf] = Counter()
        consolidado_uf_ano[uf][ano] += processos
        if regiao not in consolidado_regiao_ano:
            consolidado_regiao_ano[regiao] = Counter()
        consolidado_regiao_ano[regiao][ano] += processos
    dict_to_csv(consolidado_uf, ['uf', 'processos'],
                arquivo_consolidado_uf, 'processos', 'desc')
    dict_to_csv(consolidado_regiao, ['regiao', 'processos'],
                arquivo_consolidado_regiao, 'processos', 'desc')

    titulo = 'Processos de Juizados Especiais - {} a {}'.format(min(anos), max(anos))
    p = Plotter(arquivo_consolidado_uf)
    p.scatter(x_column='uf', x_label='Unidade Federativa', y_lim=(0, 32000),
              y_label=u'Número de processos', title=titulo, legends=None)
    p.save('graficos/processos-juizados-especiais-por-uf.png')
    log('OK\n', date_and_time=False)

    log('Criando gráfico consolidado por região... ')
    p = Plotter(arquivo_consolidado_regiao)
    p.pie('processos', 'regiao', titulo)
    p.save('graficos/processos-juizados-especiais-por-regiao.png')
    log('OK\n', date_and_time=False)

    log('Criando gráficos por UF...\n')
    for uf, data in consolidado_uf_ano.iteritems():
        log('  ' + uf + '\n')
        arquivo = 'dados-consolidados/processos-juizados-especiais-por-uf-{}.csv'.format(uf)
        tabela_uf = Table(headers=['ano', 'processos'])
        tabela_uf.extend(data.items())
        anos_que_faltam = anos - set(tabela_uf['ano'])
        for ano in anos_que_faltam:
            tabela_uf.append((ano, 0))
        tabela_uf.order_by('ano')
        tabela_uf.write('csv', arquivo)
        p = Plotter(arquivo)
        p.scatter(x_column='ano', x_label='Ano', y_lim=(0, None),
                  y_label=u'Número de processos',
                  title='Processos de Juizados Especiais - {}'.format(uf),
                  legends=None)
        p.save('graficos/processos-juizados-especiais-por-uf-{}.png'.format(uf))

    log('Criando gráficos por região...\n')
    for regiao, data in consolidado_regiao_ano.iteritems():
        log('  ' + regiao + '\n')
        arquivo = 'dados-consolidados/processos-juizados-especiais-por-regiao-{}.csv'.format(regiao)
        anos_que_faltam = anos - set(data.keys())
        for ano in anos_que_faltam:
            data[ano] = 0
        dict_to_csv(data, ['ano', 'processos'], arquivo, 'ano')
        p = Plotter(arquivo)
        p.scatter(x_column='ano', x_label='Ano', y_lim=(0, None),
                  y_label=u'Número de processos',
                  title='Processos de Juizados Especiais - {}'.format(regiao),
                  legends=None)
        p.save('graficos/processos-juizados-especiais-por-regiao-{}.png'.format(regiao))

    log('Criando gráfico de juizados especiais ativos... ')
    arquivo = 'dados-consolidados/juizados-especiais-ativos.csv'
    titulo = 'Juizados Especiais Ativos'
    tabela_ativos = Table()
    tabela_ativos.read('csv', 'dados/juizados-especiais-ativos.csv')
    tabela_ativos_2 = Table(headers=tabela_ativos.headers)
    outros = 0
    for registro in tabela_ativos:
        processos = registro[1]
        if processos < 50:
            outros += processos
        else:
            tabela_ativos_2.append(registro)
    tabela_ativos_2.append(('Outros', outros))
    tabela_ativos_2.order_by(tabela_ativos_2.headers[1], 'desc')
    tabela_ativos_2.write('csv', arquivo)
    p = Plotter(arquivo, width=1600, height=1200)
    p.pie(tabela_ativos_2.headers[1], tabela_ativos_2.headers[0], titulo)
    p.save('graficos/juizados-especiais-ativos.png')
    log('OK\n', date_and_time=False)

    log('Done!\n')

def deleta_e_cria_diretorio(diretorio):
    try:
        rmtree(diretorio)
    except OSError:
        pass
    mkdir(diretorio)


if __name__ == '__main__':
    deleta_e_cria_diretorio('graficos')
    deleta_e_cria_diretorio('dados-consolidados')
    gera_graficos()
