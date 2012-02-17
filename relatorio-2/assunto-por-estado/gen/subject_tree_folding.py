'''
Created on Jan 17, 2012

@author: cyg
'''
from __future__ import division
from SENutils import load_csv
from SENutils import write_to_csv


repository = {}
cleanRootRepo = {}
rootRepo = {}
rootRepoByState = {}
###############################################################################
def blah(item):
    return item[1]
def run():
    resultSet = load_csv('pre-dados/todos_os_assuntos_da_raiz_a_folha.csv')
    map(updateCount, resultSet[1:])
    for state,bystateitems in rootRepoByState.items():
        write_to_csv('csv/misc/estados/',state+'_FINALassunto.csv', ['COLUNA A','COLUNA B' ], bystateitems.items())
    pass
#    *******************
    count = 0
    totalMax = 0
    for state,bystateitems in rootRepoByState.items():
        sum = 0
        sortedItems = sorted(bystateitems.items(), key=blah  )[::-1]
        for item in sortedItems:
            count+=1
            print count, state, '\t\t', item[0],  '\t\t', item[1]
            sum += item[1]
        print 'TOTAL for : ', state, ': ',sum
        totalMax += sum
    print 'TOTAL for ALL: ',totalMax
#    *******************
     
    pass
###############################################################################
def updateCount(countAndSubj):
    depth = 0
    if(countAndSubj[0] != '**' and countAndSubj[0] != '***'):
        if not rootRepoByState.get(countAndSubj[0]):
            rootRepoByState[countAndSubj[0]] = {}
        doUpdate( int(countAndSubj[2]), countAndSubj[1], depth=depth, state=countAndSubj[0] )
    pass
###############################################################################
def doUpdate(count, subj, depth, state):
    splitSubj = subj.rpartition("|")
    if(splitSubj[0]):
        doUpdate( count, splitSubj[0].strip(), depth+1, state )
        if repository.get(subj):
            repository[subj] = repository.get(subj)+count
        else:
            repository[subj] = count
    else:
        splitSubj = list(splitSubj)
        splitSubj[-1] = splitSubj[-1].strip()
        if(depth == 0):
            if cleanRootRepo.get(splitSubj[-1]):
                cleanRootRepo[splitSubj[-1]] = cleanRootRepo.get(splitSubj[-1])+count
            else:
                cleanRootRepo[splitSubj[-1]] = count
        if repository.get(splitSubj[-1]):
            rootRepo[splitSubj[-1]] = rootRepo.get(splitSubj[-1])+count
            repository[splitSubj[-1]] = repository.get(splitSubj[-1])+count
        else:
            rootRepo[splitSubj[-1]] = count
            repository[splitSubj[-1]] = count
            
        if rootRepoByState[state].get(splitSubj[-1]):
            rootRepoByState[state][splitSubj[-1]] = rootRepoByState[state].get(splitSubj[-1])+count
        else:
            rootRepoByState[state][splitSubj[-1]] = count
            
    
    pass
###############################################################################
def runII():
    mike = load_csv('csv/misc/checkItII.csv')
    sum = 0
    for line in mike[1:]:
        sum += int(line[0])
    print sum
###############################################################################
if __name__ == '__main__':
    run()