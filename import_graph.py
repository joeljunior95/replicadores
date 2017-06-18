# -*- coding: utf-8 -*-
from model1 import Bloco
import pandas as pd
import networkx as NX # módulo para manipular grafos
try:
    import pylab as P # módulo para auxiliar na plotagem do grafo
except ImportError:
    pass

fileName = "alb5.hcp"
filePath = "Bases/" + fileName

graphFile = open(filePath, "r")
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
B = list()
for bloco in blocos:
    b = Bloco(bloco)
    B.append(b)

for b in B:
    print(b.get_value(), "type:", type(b.get_value()))



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
