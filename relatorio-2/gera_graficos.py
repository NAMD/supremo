#!/usr/bin/env python
# coding: utf-8

from plotter import Plotter


arquivo = 'processos_por_estado_por_ano/processos_por_uf_2000_a_2010.csv'
p = Plotter(arquivo, rows=3, cols=1)
p.scatter(x_column='uf', title='Processos por UF de 2000 a 2010',
          order_by='uf', ordering='asc', labels=False, legends=None)
p.scatter(x_column='uf', title='',
          order_by='processos', ordering='desc', labels=False, legends=None)
total_processos = float(sum(p.data['processos']))
p.data['processos'] = [100 * x / total_processos for x in p.data['processos']]
p.data.order_by('processos', 'desc')
p.bar(x_column='uf', title='', legends=None, y_label='Percentual de processos',
      y_lim=(0, 30))
p.save(arquivo.replace('.csv', '.png'))

processos_por_estado = ['processos_por_estado_2000.csv',
                        'processos_por_estado_2001.csv',
                        'processos_por_estado_2002.csv',
                        'processos_por_estado_2003.csv',
                        'processos_por_estado_2004.csv',
                        'processos_por_estado_2005.csv',
                        'processos_por_estado_2006.csv',
                        'processos_por_estado_2007.csv',
                        'processos_por_estado_2008.csv',
                        'processos_por_estado_2009.csv']
for arquivo in processos_por_estado:
    arquivo = 'processos_por_estado_por_ano/' + arquivo
    p = Plotter(arquivo, rows=3, cols=1)
    ano = arquivo.split('_')[-1].split('.')[0]
    p.data.order_by('uf')
    p.scatter(x_column='uf', title='Processos por UF de ' + ano,
              order_by='uf', ordering='asc', labels=False, legends=None,
              y_lim=(0, 160000))
    p.scatter(x_column='uf', title='', order_by='processos', ordering='desc',
              labels=False, legends=None, y_lim=(0, 160000))
    total_processos = float(sum(p.data['processos']))
    p.data['processos'] = [100 * x / total_processos for x in p.data['processos']]
    p.data.order_by('processos', 'desc')
    p.bar(x_column='uf', title='', legends=None,
          y_label='Percentual de processos', y_lim=(0, 30))
    p.save(arquivo.replace('.csv', '.png'))
