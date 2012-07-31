'''
Created on Feb 17, 2012

@author: cyg
'''
#from __future__ import division
from SENutils import load_csv
from datetime import *

def run():
    var = {}
    var2 = []
    xx = load_csv('aaa.csv')
    for x in xx[1:]:
        var[x[0]] = [x[1], x[2]]
    totaldays = None
    over = len(var.values())
    for v in var.values():
        print
        start = datetime.strptime(v[0], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(v[1], "%Y-%m-%d %H:%M:%S")
        minus = end - start
        if totaldays is None: totaldays = minus
        else: totaldays += minus
    avgTOTALdays =  totaldays.days / over
    avgyear = avgTOTALdays // 365.25
    left = avgTOTALdays % 365.25
    avgmonth = left // 30
    avgday = left % 30

    
    
    
    pass
        

if __name__ == '__main__':
    run()