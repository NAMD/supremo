#!/usr/bin/env python
# coding: utf-8

from sys import stdout
from time import strftime
from os import mkdir, path
from shutil import rmtree
from collections import Counter
from glob import glob
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

def gera_grafico_jec_consolidado(referencia, titulo, top=8):
    nova_referencia = referencia.replace('/', '-')
    arquivo_origem = 'dados/{}.csv'.format(referencia)
    arquivo_consolidado = 'dados-consolidados/{}.csv'.format(nova_referencia)
    imagem = 'graficos/{}.png'.format(nova_referencia)
    t = Table()
    t.read('csv', arquivo_origem)
    t.order_by('processos', 'desc')
    t[:] = t[:top]
    t.write('csv', arquivo_consolidado)
    p = Plotter(arquivo_consolidado)
    p.stacked_bar('origem', 'processos', y_labels='origem',
                  y_label=u'Número de processos', x_labels=None,
                  title=titulo, legend_box=(0, 1.275), legend_prop={'size': 8})
    p.save(imagem)

def gera_graficos_jec_top():
    top = 8
    log(u'Criando gráficos JEC top {}...\n'.format(top))
    log('  Brasil\n')
    titulo = u'Processos de JEC (2000 a 2009) - Brasil'
    referencia = 'processos-jec-brasil/consolidado'
    gera_grafico_jec_consolidado(referencia, titulo, top=top)
    for uf in glob('dados/processos-jec-por-uf-por-ano/*'):
        referencia = (uf + '/consolidado').replace('dados/', '')
        uf = uf.split('/')[-1]
        titulo = u'Processos de JEC (2000 a 2009) - ' + uf
        log('  {}\n'.format(uf))
        gera_grafico_jec_consolidado(referencia, titulo, top=top)
    log('  Done!\n')

def plota_jec_por_ano(referencia, titulo):
    nova_referencia = referencia.replace('/', '-')
    arquivo_consolidado = 'dados/{}/consolidado.csv'.format(referencia)
    arquivo_top5 = 'dados-consolidados/{}.csv'.format(nova_referencia)
    imagem_top5 = 'graficos/{}.png'.format(nova_referencia)
    top5 = Table()
    top5.read('csv', arquivo_consolidado)
    top5.order_by('processos', 'desc')
    top5[:] = top5[:5]
    top5 = top5['origem']
    tabela_top5 = Table(headers=['origem', 'processos', 'ano'])
    arquivos_anos = 'dados/{}/????.csv'.format(referencia)
    for arquivo_ano in glob(arquivos_anos):
        ano = int(arquivo_ano.split('/')[-1].split('.')[0])
        t = Table()
        t.read('csv', arquivo_ano)
        for r in t.to_list_of_dicts(encoding=None):
            if r['origem'] in top5:
                tabela_top5.append((r['origem'], r['processos'], ano))
    tabela_top5.order_by('ano')
    consolidada = {}
    origens = list(set(tabela_top5['origem']))
    for registro in tabela_top5:
        origem = registro[0]
        processos = registro[1]
        ano = registro[2]
        if ano not in consolidada:
            consolidada[ano] = {x: 0 for x in origens}
        consolidada[ano][origem] = processos
    tabela = Table(headers=['ano'] + origens)
    for ano, valores in consolidada.iteritems():
        valores.update({'ano': ano})
        tabela.append(valores)
    tabela.write('csv', arquivo_top5)
    p = Plotter(arquivo_top5)
    p.bar(x_column='ano', y_columns=origens, title=titulo,
          legend_box=(0, 1.35), legend_prop={'size': 8})
    p.save(imagem_top5)

def plota_jec(referencia, titulo):
    nova_referencia = referencia.replace('/', '-')
    arquivo = 'dados/{}.csv'.format(referencia)
    t = Table()
    t.read('csv', arquivo)
    anos = t['Ano']
    for ano in set(range(2000, 2010)) - set(anos):
        t.append((ano, 0))
    t.order_by('Ano')
    t.write('csv', arquivo)
    imagem = 'graficos/{}.png'.format(nova_referencia)
    p = Plotter(arquivo)
    p.scatter(x_column='Ano', title=titulo, y_label=u'Número de Processos',
              legends=None, y_lim=(0, None))
    p.save(imagem)

def gera_graficos_jec_por_ano():
    log(u'Criando gráficos por ano...\n')
    for arquivo_uf in glob('dados/*'):
        uf = arquivo_uf.split('/')[-1].split('.')[0]
        log('  {}\n'.format(uf))
        plota_jec(uf, u'Processos JEC - ' + uf)
    log(' Done!\n')

def gera_graficos_por_regiao():
    log(u'Criando gráficos por regiao...\n')
    processos_regiao = {}
    for arquivo_uf in glob('dados/*'):
        uf = arquivo_uf.split('/')[-1].split('.')[0]
        if uf == 'Brasil':
            continue
        log('  {}\n'.format(uf))
        regiao = regioes[uf]
        if regiao not in processos_regiao:
            processos_regiao[regiao] = Counter()
        tabela = Table()
        tabela.read('csv', arquivo_uf)
        for registro in tabela.to_list_of_dicts():
            processos_regiao[regiao][registro['Ano']] += registro['Processos']
    for regiao, dados in processos_regiao.iteritems():
        log('  {}\n'.format(regiao))
        arquivo = 'dados-consolidados/{}.csv'.format(regiao)
        titulo = u'Processos JEC - {}'.format(regiao.capitalize())
        imagem = 'graficos/{}.png'.format(regiao)
        for ano_faltante in set(range(2000, 2010)) - set(dados.keys()):
            dados[ano_faltante] = 0
        tabela_regiao = Table(headers=['Ano', 'Processos'])
        tabela_regiao.extend(dados.iteritems())
        tabela_regiao.write('csv', arquivo)
        p = Plotter(arquivo)
        p.scatter('Ano', title=titulo, y_label=u'Número de Processos',
                  legends=None, y_lim=(0, None))
        p.save(imagem)

    log(' Done!\n')

def gera_graficos():
    gera_graficos_jec_por_ano()
    gera_graficos_por_regiao()


if __name__ == '__main__':
    deleta_e_cria_diretorio('graficos')
    deleta_e_cria_diretorio('dados-consolidados')
    gera_graficos()
