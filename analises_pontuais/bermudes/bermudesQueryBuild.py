'''
Created on Dec 20, 2011

@author: cyg
'''
import MySQLdb

lawyer_file = open('bermudesAdvogados.txt')
rawLawyerNames = lawyer_file.readlines()
g = lambda x: x.strip('\n ').encode('UTF-8')
newLawyerNames = map( g, rawLawyerNames)


#db = MySQLdb.connect(host="10.251.1.137", user="root", passwd="mysqlFGV13",db="STF_O")
db = MySQLdb.connect(host="ssh.justen.eng.br", port=3333, user="root", passwd="mysqlFGV13",db="STF_O")

count = 1
not_found_in_db = []
found_in_db = {}
many_names_in_db_q1 = {}
many_names_in_db_q2 = {}
for lawyer_name in newLawyerNames:
    usedSecondQuery = False
#    query1= """SELECT id, nome from t_advogados where nome = '""" + lawyer_name + """'"""
    query1= """SELECT seq_jurisdicionado, nom_jurisdicionado from JURISDICIONADO where nom_jurisdicionado like '""" + lawyer_name + """' OR nom_jurisdicionado like '""" + lawyer_name + """% e %'"""
    cursor = db.cursor()
    cursor.execute(query1)
    resultSet = cursor.fetchall()
    if not resultSet:
        usedSecondQuery = True
        lawyer_tokens = lawyer_name.lower().split() 
#        query2= "SELECT id, nome from t_advogados where UCASE(nome) like UCASE('" + lawyer_tokens[0] + ' % ' + lawyer_tokens[-1] + "')"
        query2= "SELECT seq_jurisdicionado, nom_jurisdicionado from JURISDICIONADO where UCASE(nom_jurisdicionado) like UCASE('" + lawyer_tokens[0] + ' % ' + lawyer_tokens[-1] + "')"
#        print str(count) +' nothing on: ' + lawyer_name + ' ...checking with: ' + query2
        cursor.execute(query2)
        resultSet = cursor.fetchall()
    if not resultSet:
        not_found_in_db.append(lawyer_name)
    else:
        if(len(resultSet) > 1):
#            print 'para ' + lawyer_name + ' achei varios: ', list(resultSet)
            if usedSecondQuery:
                many_names_in_db_q2[lawyer_name] = list(resultSet)
            else:
                many_names_in_db_q1[lawyer_name] = list(resultSet)
            pass
        else:  
            found_in_db[lawyer_name] = resultSet[0][0]
#    print str(count)+' final results for ' + lawyer_name + ': ' + str(resultSet)
    count+=1
    cursor.close()  
print '\n\n NAO ENCONTRADOS NEM POR PRIMEIRO E ULTIMO NOME: ', len(not_found_in_db)
print '\n'.join(not_found_in_db)

print '-----ENCONTRADOS: ',len(found_in_db)
print '\n'.join(found_in_db.keys())

print '-----MULTIPLOS NOMES NO BANCO: ', len(many_names_in_db_q1)
for a in many_names_in_db_q1.items(): 
    print len(a[1]), ' : ', a[0].decode('UTF-8')
    for a1 in a[1]:
        print a1[0], a1[1].decode('UTF-8')
        
print '-----MULTIPLOS NOMES NO BANCO (COM AMBIGUIDADE): ', len(many_names_in_db_q2)
for b in many_names_in_db_q2.items(): 
    print len(b[1]), ' : ', b[0].decode('UTF-8')
    for b1 in b[1]:
        print b1[0], b1[1].decode('UTF-8')
    
#queryMontada = "SELECT * INTO tmp_levantamento_bermudes from r_processos_advogados where id_advogado = " + str(found_in_db.values()[0])
#for id in found_in_db.values()[1:]:
#    queryMontada += '\nor id_advogado = ' + str(id)
#    pass
#print '\n'
#print queryMontada


