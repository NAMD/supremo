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
<<<<<<< HEAD
from SENutils import log
=======
from strobo import SlideShow

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
>>>>>>> 0e318debded283b6b1e225d77f64299a8bd3aeb2

def plota_graficos(arquivo, imagem, titulo, total_de_processos,
                   y_lim=(0, 160000), y_lim_bar=(0, 30), titulo_bar=''):
    p = Plotter(arquivo, rows=2, cols=1)
    p.scatter(x_column='uf', title=titulo, y_label=u'Número de processos',
              labels=False, legends=None, y_lim=y_lim)
    p.data['processos'] = [100.0 * x / total_de_processos \
                           for x in p.data['processos']]
    p.bar(x_column='uf', title=titulo_bar, legends=None,
          y_label='Percentual de processos', y_lim=y_lim_bar)
    p.save(imagem)

def gera_graficos():
    log('Coletando dados... ')
    tabelas = []
    for arquivo in sorted(glob('dados/????.csv')):
        tabela = Table()
        tabela.read('csv', arquivo)
        ano = path.basename(arquivo).split('-')[-1].split('.')[0]
        imagem = 'graficos/' + path.basename(arquivo.replace('.csv', '.png'))
        tabelas.append({'ano': ano, 'imagem': imagem,
                        'total_de_processos': sum(tabela['processos']),
                        'tabela': tabela})
    anos = [info['ano'] for info in tabelas]
    range_anos = (min(anos), max(anos))
    log('OK\n', date_and_time=False)

    log('Criando gráfico consolidado... ')
    processos = Counter()
    processos_por_regiao = Counter()
    tabela_uf = {}
    for info in tabelas:
        for registro in info['tabela'].to_list_of_dicts():
            uf = registro['uf']
            processos[uf] += registro['processos']
            if uf not in tabela_uf:
                tabela_uf[uf] = Table(headers=['ano', 'processos'])
            tabela_uf[uf].append((info['ano'], registro['processos']))
            if uf in regioes:
                regiao = regioes[uf]
                processos_por_regiao[regiao] += registro['processos']

    tabela_consolidada = Table(headers=['uf', 'processos'])
    for item in processos.iteritems():
        tabela_consolidada.append(item)
    tabela_consolidada.order_by('processos', 'desc')
    arquivo = 'dados-consolidados/processos-por-uf-geral.csv'
    tabela_consolidada.write('csv', arquivo)
    plota_graficos(arquivo,
                   'graficos/consolidado.png',
                   'Processos por UF - {} a {}'.format(min(anos), max(anos)),
                   y_lim=(0, 200000),
                   total_de_processos=sum(tabela_consolidada['processos']))

    tabela_por_regiao = Table(headers=['regiao', 'processos'])
    for item in processos_por_regiao.iteritems():
        tabela_por_regiao.append(item)
    arquivo = 'dados-consolidados/processos-por-regiao.csv'
    tabela_por_regiao.write('csv', arquivo)
    p = Plotter(arquivo)
    p.pie('processos', 'regiao',
          title=u'Processos por região geográfica ({} a {})'.format(*range_anos))
    p.save('graficos/processos-por-regiao.png')
    log('OK\n', date_and_time=False)

    log('Criando gráficos por UF...')
    pib_por_ano = {}
    tabela_pib = Table()
    tabela_pib.read('csv', '../../dados-externos/pib-por-uf-por-ano.csv')
    for r in tabela_pib.to_list_of_dicts():
        if r['uf'] not in pib_por_ano:
            pib_por_ano[r['uf']] = {}
        pib_por_ano[r['uf']][r['ano']] = r['pib']
    pea_por_ano = {}
    tabela_pea = Table()
    tabela_pea.read('csv', '../../dados-externos/populacao-economicamente-ativa-por-uf-por-ano.csv')
    for r in tabela_pea.to_list_of_dicts():
        if r['uf'] not in pea_por_ano:
            pea_por_ano[r['uf']] = {}
        pea_por_ano[r['uf']][r['ano']] = r['populacao']
    for uf, tabela in tabela_uf.iteritems():
        arquivo = 'dados-consolidados/por-uf-{}.csv'.format(uf)
        tabela.write('csv', arquivo)
        p = Plotter(arquivo, rows=3, cols=1)
        p.scatter(x_column='ano', title=u'Processos por Ano - {}'.format(uf),
                  y_label=u'Número de processos', labels=False, legends=None,
                  y_lim=(0, None))
        backup = []
        for r in p.data:
            backup.append(r[1])
            r[1] = r[1] / (pib_por_ano[uf][r[0]] / 1000000.0)
        p.scatter(x_column='ano', y_label=u'Processos / PIB (milhões)',
                  x_label='', legends=None, y_lim=(0, None))
        pea_2001 = float(pea_por_ano[uf][2001])
        pea_2002 = pea_por_ano[uf][2002]
        pea_por_ano[uf][2000] = pea_2001 / (pea_2002 / pea_2001)
        for indice, r in enumerate(p.data):
            r[1] = backup[indice] / (pea_por_ano[uf][r[0]] / 1000000.0)
        p.scatter(x_column='ano',
                  y_label=u'Processos / PEA (milhões)',
                  x_label='', legends=None, y_lim=(0, None))
        p.save('graficos/por-uf-{}.png'.format(uf))
    log('OK\n', date_and_time=False)

    log('Criando gráficos por ano...\n')
    ufs = tabela_consolidada['uf']
    for info in tabelas:
        log('  {}... '.format(info['ano']))
        arquivo = 'dados-consolidados/{}.csv'.format(info['ano'])
        processos = {}
        for registro in info['tabela'].to_list_of_dicts():
            processos[registro['uf']] = registro['processos']
        t = Table(headers=['uf', 'processos'])
        for uf in ufs:
            t.append((uf, processos[uf]))
        t.write('csv', arquivo)
        p = plota_graficos(arquivo, info['imagem'],
                           'Processos por UF - ' + info['ano'],
                           total_de_processos=info['total_de_processos'],
                           y_lim=(0, 30000))
        log('OK\n', date_and_time=False)
    log('Done!\n')

    log('Definindo portes das UFs... ')
    total_de_processos = float(sum(tabela_consolidada['processos']))
    grande_porte = [registro[0] for registro in tabela_consolidada[:4]]
    del tabela_consolidada[:4]
    for indice, registro in enumerate(tabela_consolidada.to_list_of_dicts()):
        if registro['processos'] / total_de_processos <= 0.01:
            break
    pequeno_porte = [registro[0] for registro in tabela_consolidada[indice:]]
    del tabela_consolidada[indice:]
    medio_porte = [registro[0] for registro in tabela_consolidada]
    del tabela_consolidada
    log('OK\n', date_and_time=False)

    log('Separando portes por ano e gerando gráficos...\n')
    pequeno_consolidado_uf = Counter()
    medio_consolidado_uf = Counter()
    grande_consolidado_uf = Counter()
    consolidado_ano = Table(headers=['Ano', 'Pequeno Porte', u'Médio Porte',
                                     'Grande Porte'])
    for info in tabelas:
        log('  {}: '.format(info['ano']))
        t = info['tabela']
        total_de_processos = sum(t['processos'])
        tabela_grande_porte = Table(headers=t.headers)
        tabela_medio_porte = Table(headers=t.headers)
        tabela_pequeno_porte = Table(headers=t.headers)
        dados = {}
        for registro in t.to_list_of_dicts():
            dados[registro['uf']] = registro['processos']
        for uf in pequeno_porte:
            tabela_pequeno_porte.append((uf, dados[uf]))
        for uf in medio_porte:
            tabela_medio_porte.append((uf, dados[uf]))
        for uf in grande_porte:
            tabela_grande_porte.append((uf, dados[uf]))
        for registro in tabela_pequeno_porte.to_list_of_dicts():
            pequeno_consolidado_uf[registro['uf']] += registro['processos']
        for registro in tabela_medio_porte.to_list_of_dicts():
            medio_consolidado_uf[registro['uf']] += registro['processos']
        for registro in tabela_grande_porte.to_list_of_dicts():
            grande_consolidado_uf[registro['uf']] += registro['processos']
        consolidado_ano.append((info['ano'],
                                sum(tabela_pequeno_porte['processos']),
                                sum(tabela_medio_porte['processos']),
                                sum(tabela_grande_porte['processos'])))
        p = 'dados-consolidados/pequeno-porte-{}.csv'.format(info['ano'])
        m = 'dados-consolidados/medio-porte-{}.csv'.format(info['ano'])
        g = 'dados-consolidados/grande-porte-{}.csv'.format(info['ano'])
        nome_p = 'graficos/' + path.basename(p.replace('.csv', '.png'))
        nome_m = 'graficos/' + path.basename(m.replace('.csv', '.png'))
        nome_g = 'graficos/' + path.basename(g.replace('.csv', '.png'))
        tabela_pequeno_porte.write('csv', p)
        tabela_medio_porte.write('csv', m)
        tabela_grande_porte.write('csv', g)
        plota_graficos(p, nome_p,
                       'Processos de {} - Pequeno Porte'.format(info['ano']),
                       y_lim=(0, 4000),
                       total_de_processos=info['total_de_processos'],
                       y_lim_bar=(0, 3.5), titulo_bar='Percentual no ano')
        plota_graficos(m, nome_m,
                       u'Processos de {} - Médio Porte'.format(info['ano']),
                       y_lim=(0, 12000),
                       total_de_processos=info['total_de_processos'],
                       y_lim_bar=(0, 12), titulo_bar='Percentual no ano')
        plota_graficos(g, nome_g,
                       'Processos de {} - Grande Porte'.format(info['ano']),
                       y_lim=(0, 30000),
                       total_de_processos=info['total_de_processos'],
                       y_lim_bar=(0, 25), titulo_bar='Percentual no ano')
        log('OK\n', date_and_time=False)

    log('Criando gráfico consolidado de portes... ')
    arquivo = 'dados-consolidados/processos-por-porte-consolidado-por-ano.csv'
    consolidado_ano.write('csv', arquivo)
    p = Plotter(arquivo, rows=4, cols=1, width=1600, height=1200)
    p.bar(x_column='Ano', legends=False,
          title=u'Pequeno Porte ({} a {})'.format(*range_anos),
          bar_width=0.5, y_columns=['Pequeno Porte'], colors=['r'])
    p.bar(x_column='Ano', legends=False,
          title=u'Médio Porte ({} a {})'.format(*range_anos),
          bar_width=0.5, y_columns=[u'Médio Porte'], colors=['g'])
    p.bar(x_column='Ano', legends=False,
          title=u'Grande Porte ({} a {})'.format(*range_anos),
          bar_width=0.5, y_columns=['Grande Porte'], colors=['b'])
    p.bar(x_column='Ano', legends=True,
          title=u'Todos os Portes ({} a {})'.format(*range_anos),
          bar_width=0.5,
          y_columns=['Pequeno Porte', u'Médio Porte', 'Grande Porte'],
          colors=['r', 'g', 'b'])
    p.save('graficos/consolidado-por-porte.png')
    log('OK\n', date_and_time=False)
    log('Done!\n')

def gera_animacao():
    # sudo aptitude install ffmpeg2theora
    log('Creating slideshow... ')
    slides = SlideShow(delay=2.05, size=(2000, 1200), fade_in=1, fade_out=1)
    log('OK\n', date_and_time=False)

    log('  Adding images... ')
    slides.add_images('graficos/????.png', 'graficos/consolidado.png')
    log('OK\n', date_and_time=False)

    log('  Creating images... ')
    slides.create_images()
    log('OK\n', date_and_time=False)

    log('Rendering video... ')
    slides.render('graficos/processos-por-uf')
    log('OK\n', date_and_time=False)

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
    gera_animacao()
