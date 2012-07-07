#!/usr/bin/env python
# coding: utf-8

from sys import stdout
from time import strftime
from os import mkdir, path
from shutil import rmtree
from glob import glob
from plotter import Plotter


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
    for arquivo_uf in glob('dados/??.csv'):
        uf = arquivo_uf.split('/')[-1].split('.')[0]
        log(u'Criando gráfico para {}...\n'.format(uf))
        p = Plotter(arquivo_uf)
        p.scatter(title=u'Top Litigantes {}'.format(uf),
                  x_column='nome', x_label='Litigante', y_label='Processos')
        p.save('graficos/{}.png'.format(uf))

if __name__ == '__main__':
    deleta_e_cria_diretorio('graficos')
    gera_graficos()
