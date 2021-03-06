# -*- coding:utf-8 -*-
'''
Created on Jan 5, 2012

@author: cyg
'''
import MySQLdb
import csv
import os
from sys import stdout
from time import strftime
###############################################################################
def senDbConn(name="STF_O", flagRemoteSSH=False):
    if flagRemoteSSH:
        return MySQLdb.connect(host="ssh.justen.eng.br", port=3333, user="root", passwd="mysqlFGV13",db=name)
    else:
        return MySQLdb.connect(host="10.251.1.137", user="root", passwd="mysqlFGV13",db=name)
###############################################################################
STATE_CODES = {
        'Acre':'AC',
        'Alagoas':'AL',
        'Amapá':'AP',
        'Amazonas':'AM',
        'Bahia' :'BA',
        'Ceará':'CE',
        'Distrito Federal' :'DF',
        'Espírito Santo':'ES',
        'Goiás':'GO',
        'Maranhão':'MA',
        'Mato Grosso':'MT',
        'Mato Grosso do Sul':'MS',
        'Minas Gerais':'MG',
        'Pará':'PA',
        'Paraíba':'PB',
        'Paraná':'PR',
        'Pernambuco':'PE',
        'Piauí':'PI',
        'Rio de Janeiro':'RJ',
        'Rio Grande do Norte':'RN',
        'Rio Grande do Sul':'RS',
        'Rondônia':'RO',
        'Roraima':'RR',
        'Santa Catarina':'SC',
        'São Paulo':'SP',
        'Sergipe':'SE',
        'Tocantins':'TO',
}

STATE_REGIONS ={
        'Acre':'Norte',
        'Alagoas':'Nordeste',
        'Amapá':'Norte',
        'Amazonas':'Norte',
        'Bahia' :'Nordeste',
        'Ceará':'Nordeste',
        'Distrito Federal' :'Centro-Oeste',
        'Espírito Santo':'Sudeste',
        'Goiás':'Centro-Oeste',
        'Maranhão':'Nordeste',
        'Mato Grosso':'Centro-Oeste',
        'Mato Grosso do Sul':'Centro-Oeste',
        'Minas Gerais':'Sudeste',
        'Pará':'Norte',
        'Paraíba':'Nordeste',
        'Paraná':'Sul',
        'Pernambuco':'Nordeste',
        'Piauí':'Nordeste',
        'Rio de Janeiro':'Sudeste',
        'Rio Grande do Norte':'Nordeste',
        'Rio Grande do Sul':'Sul',
        'Rondônia':'Norte',
        'Roraima':'Norte',
        'Santa Catarina':'Sul',
        'São Paulo':'Sudeste',
        'Sergipe':'Nordeste',
        'Tocantins':'Norte',
}

STATE_KEYS = {
        'AC':2,
        'AL':4,
        'AM':8,
        'AP':6,
        'BA':10,
        'CE':12,
        'DF':14,
        'ES':16,
        'GO':20,
        'MA':22,
        'MG':28,
        'MS':26,
        'MT':24,
        'PA':30,
        'PB':32,
        'PE':36,
        'PI':38,
        'PR':34,
        'RJ':7,
        'RN':40,
        'RO':46,
        'RR':48,
        'RS':42,
        'SC':50,
        'SE':54,
        'SP':52,
        'TO':56
}

###############################################################################
def load_csv(filename, lines=None, encoding=None):
    """
    Abre Arquivo csv primeira linha deve ser cabecalho com nomes de variaveis
    retorna uma lista
    """
    fp = open(filename)
    reader = csv.reader(fp)
    myList = []
    if lines:
        for x in range(lines):
            y = x; y += y
            try: line = reader.next()
            except: break
            myList.append(line)
            
#            if encoding : map(
#                              lambda x: x.decode(encoding), line)
#            list.append(line)
        data = myList
    else:
        data = list(reader)
    fp.close()
    return data
###############################################################################
def write_to_csv(location, name, columnTitles, data):
    if not os.path.exists(location):
        os.makedirs(location)
    writer = csv.writer(open(location+name, 'wb'))
    writer.writerow( columnTitles )
    writer.writerows(data)
###############################################################################
def log(text, date_and_time=True):
    if date_and_time:
        stdout.write('[%s] %s' % (strftime('%Y-%m-%d %H:%M:%S'), text))
    else:
        stdout.write(text)
    stdout.flush()
###############################################################################
# INSTANTIATING INLINE OBJECTS IN PYTHON::::
# obj = type('obj', (object,), {'propertyName' : 'propertyValue'})
###############################################################################


        