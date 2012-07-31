#!/usr/bin/env python
# coding: utf-8
'''
Created on Jul 10, 2012

@author: cyg
'''
from glob import glob
from outputty import Table
from SENutils import deleta_e_cria_diretorio, log
from sys import stdout
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from pylab import *
###############################################################################
def gera_graficos():
    for arquivo_uf in glob('dados/??.csv'):
        uf = arquivo_uf.split('/')[-1].split('.')[0]
#        log(u'Criando gráfico para {}...\n'.format(uf))
        dataTable = Table()
        dataTable.read('csv', arquivo_uf)
        
        fig = bar(data=dataTable.data[1:10], x_label='litigante', y_label=dataTable.headers[1], title=u'Top Litigantes {} 2000 a 2009'.format(uf))
        fig.savefig('graficos/{}.png'.format(uf))
###############################################################################
#def barh(data=None, order_by=None, ordering='asc', title='', x_label='', y_label='', width=1024 , height=768):
#    fig = figure(figsize=(width / 80, height / 80), dpi=80)
#    
#    subplot = fig.add_subplot(111)
#    subplot.set_title(title, fontsize=24)
#    subplot.grid(True)
#    
#    if order_by is not None:
#        data.order_by(order_by, ordering)
#    
#    val = 3+10*rand(5)    # the bar lengths
#    pos = arange(len(data))+.5    # the bar centers on the y axis
#    
#    subplot.set_xlabel(x_label)
#    subplot.set_ylabel(y_label)
#    fig.subplots_adjust(top=0.92, bottom=0.22, right=0.95, left=0.325)
#    
#    barh(pos,[int(x[1]) for x in data], align='center', color='purple')
#    yticks(pos, [unicode(x[0]) for x in data] )
#    xlabel(x_label)
#    return fig
###############################################################################
def bar(data=None, order_by=None, ordering='asc', title='', x_label='', y_label='', width=1024 , height=768):
    
    if order_by is not None:
        data.order_by(order_by, ordering)

    fig = figure(figsize=(width / 80, height / 80), dpi=80)
    subplot = fig.add_subplot(111)
    subplot.set_title(title, fontsize=24)
    subplot.grid(True)
    
    subplot.set_xlabel(x_label)
    subplot.set_ylabel(y_label)
    pos = arange(len(data))+.5    # the bar centers on the y axis
    xticks(pos, [unicode(x[0]) for x in data], rotation=45 )
    subplot.set_title(title, fontsize=24)
    fig.subplots_adjust(top=0.92, bottom=0.4, right=0.95, left=0.085)
    
    subplot.bar(pos,[int(x[1]) for x in data], align='center', color='purple')
    fig.autofmt_xdate()
    return fig
    
###############################################################################
if __name__ == '__main__':
    deleta_e_cria_diretorio('graficos')
    gera_graficos()
    pass