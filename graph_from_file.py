# -*- coding: utf-8 -*-
import pandas as pd
import networkx as NX # módulo para manipular grafos
try:
    import pylab as P # módulo para auxiliar na plotagem do grafo
except ImportError:
    pass

fileName = "alb5.hcp"

graphFile = open(fileName, "r")
graphList = list(graphFile)
del graphList[0:6]
del graphList[-2:]

verticesList = list()

for edge in graphList:
    vertices = edge.split()
    verticesList.append(vertices)

G=NX.Graph()

for v in verticesList:
    G.add_edge(v[0], v[1])

blocos = G.nodes() + G.edges()
print(blocos)


"""
try:
    pos=NX.spring_layout(G)
    NX.draw(G,pos,font_size=16,with_labels=False)
#     for p in pos: # raise text positions
#         pos[p][1]+=0.07
    NX.draw_networkx_labels(G,pos)
    P.show()
except:
    pass
"""
