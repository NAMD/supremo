# -*- coding:utf-8 -*-
from __future__ import division
from SENutils import senDbConn
from SENutils import load_csv
import matplotlib.pyplot as plt
import numpy as np
import csv
import string
import sys
import matplotlib.cm as cm
###############################################################################
#    Federal Constitution of 1988 (id 1): cited 166180 times;
#    Civil Code (id 2): cited 92772 times;
#    Penal Code (id 9): cited 11349 times;
#    Code of Processo Penal(id 10): cited 10117 times;
#    Sumula 288 - inadmissão de agravo em RE (id 11): cited 9328 times
#    Federal Constitution of 1969 (id 15): cited 6435 times.
###############################################################################

START_YEAR = 1988
END_YEAR = 2010

query = """SELECT year(data_dec) "ano", count(numero) "num citações" 
FROM artigo_lei, lei_decisao, decisao  
where lei = 'CF' 
and lei_decisao.ano = 1988  
and year(data_dec) >= """ + str(START_YEAR) + """ and year(data_dec) <= """ + str(END_YEAR) + """ and artigo_lei.lei_id = lei_decisao.id
and lei_decisao.decisao_id = decisao.id
and artigo_lei.numero = '%s'
group by year(data_dec)  
order by year(data_dec) """
#"count" desc """ 
###############################################################################
out=lambda *x:\
    sys.stdout.write(" ".join(map(str,x))+"\n")
###############################################################################
SIZE = 5#len(lines)
###############################################################################
def viz(lines):
    STARTIDX = 0    
    
    lines = lines[STARTIDX:SIZE]
    plt.rcParams['font.size'] = 8
    all_lines = []
    total_cites_4allArticles_per_year = {}
    for article, t_year_cites in lines:
        yearOfCitation, yearlyCitationCount = zip(*t_year_cites)  
        yearlyCitationCountList = list(yearlyCitationCount)
        range_of_years = range(START_YEAR, END_YEAR+1)
        if( len(t_year_cites) <= (END_YEAR-START_YEAR) ):
        #garantindo que todos os anos estão presentes e inserindo 0 onde não
            anoList = list(yearOfCitation)
            for idx,curYear in enumerate(range_of_years):
                if idx == 0 and anoList[0] != START_YEAR:
                    anoList.insert(0, START_YEAR)
                    yearlyCitationCountList.insert(idx, 0)
                elif(idx != 0 and curYear != anoList[idx]):
                    anoList.insert(idx, range_of_years[idx])
                    yearlyCitationCountList.insert(idx, 0)
            try:
                total_cites_4allArticles_per_year[curYear] = total_cites_4allArticles_per_year[curYear] + yearlyCitationCountList[idx]
                ill = 0; ill+=1
            except KeyError:
                total_cites_4allArticles_per_year[curYear] = yearlyCitationCountList[idx]
        all_lines.append( [yearlyCitationCountList, article] )
        
    fig = plt.figure(None, (12,9), 100)
    fig.subplots_adjust(bottom=0.1, left=.2)
    fig.suptitle("Artigos Mais Citados da CF '88 por Ano".decode('UTF-8'), fontsize=20)
    
    yearly_totals = load_csv("pre-dados/totais_artigosDaCF_por_ano.csv")
    cleanYearlyTotals = zip(zip(*yearly_totals[1:])[0], zip(*yearly_totals[1:])[2])
    percentStackedBars(range_of_years, all_lines, fig, cleanYearlyTotals)
    
    stackedBars(range_of_years, all_lines, fig)
    plt.show()
    pass
###############################################################################
xAxisPlacementForLegend = -0.25
yAxisPlacementForLegend = 1.005
colormap = cm.hsv
###############################################################################
def percentStackedBars(range_of_years, all_lines, fig, cleanYearlyTotals):
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(all_lines)+1)]
    
    ax = fig.add_subplot(212)
    ax.set_xlabel('Ano')
    ax.set_ylabel('Porcentagem de Citações'.decode('UTF-8'), fontsize=15)
    ax.set_xticks( range_of_years )
    a = np.linspace(0,1,11)
    ax.set_yticks( a )
    ax.set_xticklabels( range_of_years, rotation=45) 
    ax.set_xticklabels( [x for x in range_of_years] )

    justTheTotals = [x[1] for x in cleanYearlyTotals]
    count = 0

    bottomBar = [0]*len(all_lines[0][0])
    remainderOfTotal = list(justTheTotals)
    for curLine in all_lines:
        curPercentLine = [long(y[1])/long(y[0]) for y in zip(justTheTotals,curLine[0])]
        ax.bar( range_of_years, curPercentLine, width=0.35, label='art'+str(curLine[1]), bottom=bottomBar, color=colors[count])
        remainderOfTotal = [int(x[0])-int(x[1]) for x in zip(remainderOfTotal, curLine[0])]
        bottomBar = [sum(a) for a in zip(bottomBar,curPercentLine)]
        count+=1
    percentOther = [long(y[0])/long(y[1]) for y in zip(remainderOfTotal,justTheTotals)]
    ax.bar( range_of_years,percentOther, width=0.35, label='outros', bottom=bottomBar, color=colors[count])
###############################################################################
def stackedBars(range_of_years, all_lines, fig):
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(all_lines)+1)]
    
    ax = fig.add_subplot(211)
    ax.set_xlabel('Ano')
    ax.set_ylabel('Número de Citações'.decode('UTF-8'), fontsize=15)
    ax.set_xticks( range_of_years )
    ax.set_xticklabels( range_of_years, rotation=45) 
    
    # http://matplotlib.sourceforge.net/examples/pylab_examples/show_colormaps.html
    count = 0
    ax.bar( range_of_years,all_lines[0][0], width=0.35, label='art'+str(all_lines[0][1]), color=colors[count])
    bottomBar = [0]*len(all_lines[0][0])
    for line in all_lines[1:]:
        count+=1
        bottomBar = [sum(a) for a in zip(bottomBar,all_lines[count-1][0])]
        ax.bar( range_of_years,line[0], width=0.35, label='art'+str(line[1]), color=colors[count], bottom=bottomBar)
    ax.legend(loc='upper left',bbox_to_anchor = (xAxisPlacementForLegend, yAxisPlacementForLegend))
###############################################################################
def write_to_csv(article_number, total_citations, resultList):
    writer = csv.writer(open('dados/ART-'+article_number+'_total-'+total_citations+'.csv', 'wb'))
    writer.writerow( ('ano','citações') )
    writer.writerows(resultList)
###############################################################################
def process_data(data, writing_to_csv, process_top_X=100):
    results = []
    for datum in data[1:process_top_X]:
        curQuery = query % datum[1]
        db = senDbConn("STF_Analise_Decisao", flagRemoteSSH= True)
        cursor = db.cursor()
        cursor.execute(curQuery)
        resultSet = cursor.fetchall()
        if writing_to_csv: write_to_csv(datum[1], datum[2], list(resultSet))
        list(resultSet)
        
        
        result = (datum[1],resultSet)
        results.append(result)
    return results
###############################################################################
def run():
    data = load_csv('pre-dados/top_100_artCitadosDaCF.csv')
    results = process_data(data, writing_to_csv=False)
    viz(results)
    
###############################################################################
if __name__ == '__main__':
    run()



