# -*- coding:utf-8 -*-
'''
Created on 05/04/2011

@author: flavio
'''
'''
Configurações:
'''
confs = "Flavio"

if confs == "Flavio":
    ubiServer = "http://10.250.46.208:20738/RPC2"
    MySQLServer = "mysql://root:password@E04324"

if confs == "Pablo":
    ubiServer = "http://127.0.0.1:20738/RPC2"
    MySQLServer = "mysql://pablo:pablo@E04324.fgv.br"

'''
Final das configurações
'''

import networkx as nx
import xmlrpclib
import os, time
from sqlalchemy.ext.sqlsoup import SqlSoup
import numpy as np
import matplotlib.pyplot as P
from matplotlib.colors import rgb2hex
from matplotlib import cm
import ubigraph
import cPickle
import gzip

cf88_vs_outras_q = """
select 
  1 lei_id_1, ld_1.lei_id lei_id_2, count(ld_1.lei_id) peso
from 
  lei_decisao ld_1
where 
  ld_1.decisao_id in (
    select 
      ld_2.decisao_id
    from
      lei_decisao ld_2
    where
      ld_2.lei_id = 1
  ) and
  ld_1.lei_id <> 1
group by
  ld_1.lei_id
order by
  count(ld_1.lei_id) desc
"""

def timeit(fun):
    """
    Decorator to time methods (or functions)
    """
    def timed(*args, **kw):
        ts = time.time()
        result = fun(*args, **kw)
        te = time.time()
        print '%r (%s,%s)  %2.2f sec'%(fun.__name__, args, kw , te-ts)
        return result
    return timed

def dyn_graph_lei(elist):
    """
    Visualização dinâmica usando ubigraph
    Servidor Ubigraph deve estar rodando na URL indicada
    """
    U = ubigraph.Ubigraph(URL=ubiServer)
    U.clear()
    ''' Versão 1 '''
    v_styles = {'LEG-FED':U.newVertexStyle(id=1,shape="cube", color="#ff0000"),
                'LEG-EST':U.newVertexStyle(id=2,shape="cube", color="#00ff00"),
                'LEG-MUN':U.newVertexStyle(id=3,shape="cube", color="#0000ff"),
                'LEG-DIS':U.newVertexStyle(id=4,shape="cube", color="#0ff000"),
                'LEG-INT':U.newVertexStyle(id=5,shape="cube", color="#000ff0"),
                'outras':U.newVertexStyle(id=6,shape="cube", color="#f0f000"),
                'CF':U.newVertexStyle(id=6,shape="cube", color="#00ff00"),
                }
    
    ''' Versão 2 
    v_styles = {'CF':U.newVertexStyle(id=1,shape="sphere", color="#ff0000"),
                'LEI':U.newVertexStyle(id=2,shape="sphere", color="#00ff00"),
                'SUMULA':U.newVertexStyle(id=3,shape="sphere", color="#0000ff"),
                'REGIMENTO':U.newVertexStyle(id=4,shape="sphere", color="#0ff000"),
                }
    '''
    lei_style = U.newVertexStyle(id=1,shape="sphere", color="#ff0000")
    #Q = dbgrafo.execute(cf88_vs_outras_q)
    res = elist
    nodes = {}
    edges = set([])
    #print res[0]
    maxw = float(max(np.array([i[6] for i in res]))) #largest weight
    #U.beginMultiCall()
    c = 1
    for e in res:

        if e[0] not in nodes:
            n1 = U.newVertex(style=v_styles[e[1]], label=str(e[2]))
            nodes[e[0]] = n1
        else:
            n1 = nodes[e[0]]
        if e[3] not in nodes:
            n2 = U.newVertex(style=v_styles[e[4]], label=str(e[5]))
            nodes[e[3]] = n2
        else:
            n2 = nodes[e[3]]
        es = e[6]/maxw
        if (n1,n2) not in edges:
            U.newEdge(n1,n2,spline=True,strength=es, width=2.0, showstrain=True)
            edges.add((n1,n2))
            edges.add((n2,n1))
        c += 1
    #U.endMultiCall()
    

def cf88_vs_outras(nedges):
    """
    Desenha grafo via networkx
    para grafos pequenos.
    """
    G = nx.DiGraph()
    Q = dbgrafo.execute(cf88_vs_outras_q)
    res = Q.fetchmany(nedges)#[0]
    G.add_weighted_edges_from(res)
    nx.draw(G)
    #nx.draw_graphviz(G, "fdp")
    nx.write_dot(G, 'grafo_cf_vs_outras_%s.dot'%nedges)
    P.savefig('grafo_cf_vs_outras_%s.png'%nedges)
    return G

def lei_vs_lei(nedges=None):
    """
    Grafo de todas com todas
    """
    # Verão original Flávio comentada
    # Q = dbgrafo.execute('select lei_id_1,esfera_1,lei_1,lei_id_2,esfera_2, lei_2, peso from vw_gr_lei_lei where  peso >300 and lei_id_2>2')
    # Q = dbgrafo.execute('select lei_id_1,lei_tipo_1,lei_nome_1,lei_id_2,lei_tipo_2, lei_nome_2, peso from vw_gr_lei_lei where lei_count <= 20 and lei_id_1 = 1 and lei_id_2 <= 20 limit 0,1000')
    # Q = dbgrafo.execute('select lei_id_1,lei_tipo_1,lei_nome_1,lei_id_2,lei_tipo_2, lei_nome_2, peso from vw_gr_lei_lei where lei_count <= 8 and lei_id_1 <= 20 and lei_id_2 <= 20 limit 0,1000')
    Q = dbgrafo.execute('select lei_id_1,esfera_1,lei_1,lei_id_2,esfera_2, lei_2, peso from vw_gr_lei_lei where lei_count <= 10 and lei_id_1 <= 50 and lei_id_2 <= 200 limit 0,10000')
    if not nedges:
        res = Q.fetchall()
        nedges = len(res)
    else:
        res = Q.fetchmany(nedges)
    eds = [(i[0],i[3],i[6]) for i in res]
    G = nx.Graph()
    #eds = [i[:3] for i in res]
    G.add_weighted_edges_from(eds)
    print "== Grafo Lei_Lei =="
    print "==> Order: ",G.order()
    print "==> # Edges: ",len(G.edges())

    return G,res

def artigo_artigo(nedges=None):
    """grafo de artigos de leis"""
    
    Q = dbgrafo.execute('select artigo_id_1,esfera_1,artigo_1,lei_1,artigo_id_2,esfera_2, artigo_2, lei_2, peso from vw_gr_artigo_artigo where  peso >100')
    if not nedges:
        res = Q.fetchall()
        nedges = len(res)
    else:
        res = Q.fetchmany(nedges)
    eds = [(i[0],i[4],i[8]) for i in res]
    G = nx.Graph()
    G.add_weighted_edges_from(eds)
    print "== Grafo Artigo_Artigo == "
    print "==> Order: ",G.order()
    print "==> # Edges: ",len(G.edges())
    print "==> # Cliques: ", nx.algorithms.clique.graph_number_of_cliques(G)
    print "==> Avg. Clustering: ", nx.average_clustering(G)

def salva_grafo_imagem(G):
    """
    Salva grafos em formato png e dot
    """
    nx.draw_graphviz(G)
    nx.write_dot(G, 'relatorios/grafo_lei_vs_lei.dot')
    P.savefig('relatorios/grafo_lei_vs_lei.png')
    
@timeit
def cria_grafo_de_tabela(db, tabela):
    """Cria multigrafo a partir de uma tabela no banco"""
    G = nx.MultiGraph(nome=tabela)
    Q =db.execute('select * from %s'%tabela)
    vnames  = Q.keys()
    for r in Q:
        attrs = dict(zip(vnames[1:], r[1:]))
        G.add_node(r[0], **attrs)
    return G

@timeit
def salva_grafo_db(G):
    """Salva pickle do grafo compactado"""
    gp = gzip.zlib.compress(cPickle.dumps(G, protocol=2))
    dbdec.nx_grafo.insert(nome=G.graph['nome'], grafo=gp)
    dbdec.commit()

        
@timeit
def salva_grafo_pickled(G):
    
    nx.write_gpickle(G, G.graph['nome']+'.pickle')
    
@timeit
def le_grafo_pickled(nome):
    G = nx.read_gpickle(nome+'.pickle')
    return G

@timeit
def le_grafo_do_banco(nome):
    g = dbdec.nx_grafo.filter(dbdec.nx_grafo.nome == nome).one()
    G = cPickle.loads(gzip.zlib.decompress(g.grafo))
    return G

if __name__=="__main__":
    import socket
    dbgrafo = SqlSoup("%s/SEN_Grafo" % MySQLServer)
    dbdec = SqlSoup("%s/STF_Analise_Decisao" % MySQLServer)
#    cf88_vs_outras(500)
#    dyn_graph(1000)
#    G,elist = lei_vs_lei()
#    artigo_artigo()
    G = cria_grafo_de_tabela(dbdec,'decisao')
    salva_grafo_db(G)
    G = le_grafo_do_banco('decisao')
#    salva_grafo_pickled(G)
#    Gl = cria_grafo_de_tabela(dbdec,'lei_decisao')
#    salva_grafo_pickled(Gl)
#    G = le_grafo_pickled('decisao')
    print G.order()
#    P.show()
#    dyn_graph_lei(elist)
    
