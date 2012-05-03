'''
Created on Apr 20, 2012

@author: cyg
'''

import matplotlib
import numpy as np
from pylab import grid
from pylab import legend
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
from SENutils import load_csv
from collections import defaultdict


def extract(tup):
    coords = tup[4].strip('[]').split('), (')
    coords[0] = coords[0].strip('(')
    coords[-1] = coords[-1].strip(')')
    if len(coords) == 1:
        return None
    
    y = [x.split(', ') for x in coords]
    
    clean_coords = map(lambda z: 
                       (int(z[0] or '-100')
                        ,np.float64(z[1]))
                       , y 
                       )
#    cd = defaultdict( np.float64 )
    cd = {}
    for k,v in clean_coords:
        cd[k] = v
    res = (
            int(tup[0])
            ,int(tup[1])
            ,tup[2]
            ,tup[3]
            ,cd
            )
#    if len(cd.keys()) < 10:
#        print clean_coords
#        return None
    return res
###############################################################################
my_year_map = { 1996:'orange', 2003:'green',2010:'blue'}
###############################################################################
if __name__ == '__main__':

    listt = load_csv('gensim-data/3year_coords_full_CLEAN.csv')
    Xs = []
    Ys = []
    count = 0
    cleaned = map(extract, listt[1:])
                         
    matplotlib.rcParams['axes.unicode_minus'] = False
    counter = 0
    
    a1_96_X = [];  a1_96_Y = []; a1_02_X = []; a1_02_Y = []; a1_10_X = []; a1_10_Y = []
    a2_96_X = [];  a2_96_Y = []; a2_02_X = []; a2_02_Y = []; a2_10_X = []; a2_10_Y = []
    a3_96_X = [];  a3_96_Y = []; a3_02_X = []; a3_02_Y = []; a3_10_X = []; a3_10_Y = []
    a4_96_X = [];  a4_96_Y = []; a4_02_X = []; a4_02_Y = []; a4_10_X = []; a4_10_Y = []

    for x in cleaned:
        if not x: continue
        dim_x = 0; dim_y = 1
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 1996 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a1_96_X.append( x[4].get(dim_x) )
            a1_96_Y.append( x[4].get(dim_y) )
            
        dim_x = 0; dim_y = 2
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 1996 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a2_96_X.append( x[4].get(dim_x) )
            a2_96_Y.append( x[4].get(dim_y) )
        
        dim_x = 0; dim_y = 3
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 1996 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a3_96_X.append( x[4].get(dim_x) )
            a3_96_Y.append( x[4].get(dim_y) )
       
        dim_x = 1; dim_y = 3
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 1996 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a4_96_X.append( x[4].get(dim_x) )
            a4_96_Y.append( x[4].get(dim_y) )
            
        dim_x = 0; dim_y = 1
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 2003 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a1_02_X.append( x[4].get(dim_x) )
            a1_02_Y.append( x[4].get(dim_y) )
            
        dim_x = 0; dim_y = 2
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 2003 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a2_02_X.append( x[4].get(dim_x) )
            a2_02_Y.append( x[4].get(dim_y) )
            
        dim_x = 0; dim_y = 3
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 2003 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a3_02_X.append( x[4].get(dim_x) )
            a3_02_Y.append( x[4].get(dim_y) )

        dim_x = 1; dim_y = 3
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 2003 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a4_02_X.append( x[4].get(dim_x) )
            a4_02_Y.append( x[4].get(dim_y) )
        
        dim_x = 0; dim_y = 1
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 2010 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a1_10_X.append( x[4].get(dim_x) ) 
            a1_10_Y.append( x[4].get(dim_y) )
            
        dim_x = 0; dim_y = 2
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 2010 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a2_10_X.append( x[4].get(dim_x) ) 
            a2_10_Y.append( x[4].get(dim_y) )
            
        dim_x = 0; dim_y = 3
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 2010 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a3_10_X.append( x[4].get(dim_x) ) 
            a3_10_Y.append( x[4].get(dim_y) )

        dim_x = 1; dim_y = 3
        if x[4].get(dim_x) and x[4].get(dim_y) and x[1] == 2010 and abs(x[4].get(dim_x))<50 and abs(x[4].get(dim_y))<50:
            a4_10_X.append( x[4].get(dim_x) ) 
            a4_10_Y.append( x[4].get(dim_y) )
   
    fig1 = plt.figure()
    a1 = fig1.add_subplot(221)
    a1.scatter(a1_10_X,a1_10_Y, color='orange', marker='+')
    a1.scatter(a1_02_X,a1_02_Y, color='green', marker='+')
    a1.scatter(a1_96_X,a1_96_Y, color='blue', marker='+')
    plt.xlabel('TOPIC 0')
    plt.ylabel('TOPIC 1')
    grid(True)

    
    a2 = fig1.add_subplot(222)
    a2.scatter(a2_10_X,a2_10_Y, color='orange', marker='+')
    a2.scatter(a2_02_X,a2_02_Y, color='green', marker='+')
    a2.scatter(a2_96_X,a2_96_Y, color='blue', marker='+')
    plt.xlabel('TOPIC 0')
    plt.ylabel('TOPIC 2')
    grid(True)
        
    labels = ('2010', '2003', '1996')
    legendary = legend(labels, loc=(0.6, 1.01), labelspacing=0.1)
    
    plt.figtext(0.5, 0.965,  '3-year sample plot LSI',
               ha='center', color='black', weight='bold', size='large')
#    
    a3 = fig1.add_subplot(223)
    a3.scatter(a3_10_X,a3_10_Y, color='orange', marker='+')
    a3.scatter(a3_02_X,a3_02_Y, color='green', marker='+')
    a3.scatter(a3_96_X,a3_96_Y, color='blue', marker='+')
    plt.xlabel('TOPIC 0')
    plt.ylabel('TOPIC 3')
    grid(True)
#    
    a4 = fig1.add_subplot(224)
    a4.scatter(a4_10_X,a4_10_Y, color='orange', marker='+' )
    a4.scatter(a4_02_X,a4_02_Y, color='green', marker='+' )
    a4.scatter(a4_96_X,a4_96_Y, color='blue', marker='+')
    plt.xlabel('TOPIC 1')
    plt.ylabel('TOPIC 3')
    grid(True)
    
#    fig1.set_title('3-year sample plot', )
#    a1.set_title('3-year sample plot', )
#    a1.set_title('3-year sample plot', )
#    a1.set_title('3-year sample plot', )

#    legend()
    plt.show()

