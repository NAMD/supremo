#!/usr/bin/env python
# coding: utf-8

from sys import stdout
from time import strftime
from os import mkdir, path
from shutil import rmtree
from glob import glob
from outputty import Table
from SENutils import deleta_e_cria_diretorio, log
#from plotter import Plotter
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.cm
from numpy import linspace
import datetime

###############################################################################
def gera_graficos():
    for arquivo_uf in glob('dados/??.csv'):
        uf = arquivo_uf.split('/')[-1].split('.')[0]
        log(u'Criando gráfico para {}...\n'.format(uf))
        dataTable = Table()
        dataTable.read('csv', arquivo_uf)
        
        fig = scatter(
            title=u'Top Litigantes {}'.format(uf)
            , x_column='nome'
            , x_label='Litigante'
            , y_label='Processos'
            , dataTable=dataTable
            )
        fig.savefig('graficos/{}.png'.format(uf))
###############################################################################
def scatter(width=1024
            , height=768
            , x_column=None
            , title=''
            , style='o-'
            , ignore=''
            , colors=None
            , colormap=matplotlib.cm.PRGn
            , order_by=None
            , ordering='asc'
            , x_label=None
            , y_lim=None
            , legends= None
            , legend_location='lower left'
            , legend_box=(0.16, -0.75)
            , y_label='processos'
            , x_rotation=0
            , dataTable=None
            ):
    
    fig = figure(figsize=(width / 80, height / 80), dpi=80)
    subplot = fig.add_subplot(111)
    subplot.set_title(title, fontsize=24)
    subplot.grid(True)
    
    if order_by is not None:
        self.data.order_by(order_by, ordering)
    
    if legends is None:
        legends = {row[0]: row[0] for row in dataTable._rows}
    
    if dataTable.types[x_column] in (datetime.date, datetime.datetime):
        self.fig.autofmt_xdate()
    
    if x_label is None:
        x_label = x_column
    subplot.set_xlabel(x_label)
    subplot.set_ylabel(y_label)
    
    x_values = range(1, len(dataTable[x_column]) + 1)
    subplot.set_xlim(0, max(x_values))
    
    # preparando esquema de cores para o num. de colunas
    columns_to_plot = []
    for row in dataTable._rows:
#        if row != x_column and dataTable.types[row] in (int, float):
        columns_to_plot.append(row)
    if colors is None:
        color_range = linspace(0, 0.9, len(columns_to_plot))
        colors = [colormap(i) for i in color_range]
    
    for row in dataTable._rows:
        subplot.plot(row[1:], style, label=row[0], color=colors.pop(0))
    plt.xticks(range(10), range(2000,2010))
#        plt.setp(dataTable[row], rotation=x_rotation, fontsize=8)

    if y_lim is not None:
        subplot.set_ylim(y_lim)

    subplot.legend(loc=legend_location, bbox_to_anchor=(0.00, -0.29), ncol=2, prop={'size':12})
    fig.subplots_adjust(top=0.92, bottom=0.22, right=0.9, left=0.125)
    return fig
###############################################################################
if __name__ == '__main__':
    deleta_e_cria_diretorio('graficos')
    gera_graficos()
