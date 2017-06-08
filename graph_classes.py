# -*- coding: utf-8 -*-
import pandas as pd
import networkx as NX
from random import randrange

class Soup:
    def __init__(self, fileName):
        # lambda => limiar de replicação (min de bits p/ replicar); mi => limiar de matching (min de bits pa ligar)
        self.limiar = { "lambda": 9, "mi": 2}
        self.K = 10000 # total de colisões
        self.bl = 100 # bonificação de longevidade
        self.pm = 0.01 # probabilidade de mutação
        self.m = 0.001# número gaussiano aleatório
        self.G = NX.Graph()
        self.B = list()

        self._inicializa(fileName)


        for k in range(0, self.K):
            for i in range(0, len(self.B)):
                b1 = self.B[i]
                b2 = self._randomBlock(b1)
                self.colidir(b1, b2)


    def colidir(self, b1, b2):
        edges = self.G.edges()


        vl_b1 = b1.get_value()
        if type(vl_b1) == type(""):
            vl_b1 = [vl_b1]

        vl_b2 = b2.get_value()
        if type(vl_b2) == type(""):
            vl_b2 = [vl_b2]

        for i in [0, len(vl_b1) - 1]:
            for j in [0, len(vl_b2) - 1]:
                # TODO: FAZER MÉTODO PARA COMPARAR OS DOIS VÉrtices,
                # vl_b1[i] e vl_b2[j], e um método para ligar os dois vertices
                # gerando um novo bloco.



        for e in edges:



        return



    def replicar(self, t):
        if t.tl > self.limiar["lambda"] and t.tc > 0:
            t.tc += 1
            t.tl = 0
            if t.l > 0:
                t.l += self.bl
            for x in range(0, t.L):
                t.bitsMarcados[x] = False
            if self.m <= self.pm:
                self.mutar(t)

    def mutar(self, t):
        PosMut = randrange(t.L)
        t.bits[PosMut] = self.xnor(t.bits[PosMut], 0)

    def _randomBlock(self, exception):
        j = randrange(len(self.B))

        while exception == self.B[j]:
            j = randrange(len(self.B))

        return self.B[j]

    def _inicializa(self, fileName):
        graphFile = open(fileName, "r")
        graphList = list(graphFile)
        del graphList[0:6]
        del graphList[-2:]

        verticesList = list()

        for edge in graphList:
            vertices = edge.split()
            verticesList.append(vertices)

        for v in verticesList:
            self.G.add_edge(v[0], v[1])

        blocos = self.G.nodes() + self.G.edges()

        for bloco in blocos:
            b = Bloco(bloco)
            self.B.append(b)

        return


    def xnor (self, a, b):
        return 1 if (a == b) else 0

    def matching(self, q, t, b):
        v = 0
        r = 0
        for s in range(q, q + b.c):
            if s < t.L and t.bitsMarcados[s] == False:
                r += self.xnor(t.bits[s], b.bits[v])
            v += 1
        return r
#end class Soup


class Bloco:
    def __init__(self, vertices):
        self.copies = randrange(1, 101) # número de cópias
        self.value = vertices # lista de vértices

    def get_copies(self):
        return self.copies

    def get_value(self):
        return self.value
