# -*- coding: utf-8 -*-
import pandas as pd
import networkx as NX
from random import randrange

class Soup:
    def __init__(self, fileName):
        self.K = 10000 # total de colisões
        self.limiar = {
            "lambda": 9, # limiar de replicação => qtd mínima de bits para replicar
            "mi": 2 # limiar de matching => qtd mínima de bits para ligar um bloco e um template
        }
        self.bl = 100 # bonificação de longevidade
        self.pm = 0.01 # probabilidade de mutação
        self.m = 0.001# número gaussiano aleatório
        self.G = NX.Graph()
        self.T = list()
        self.B = list()

        self._inicializa(fileName)

        lista = list()

        for k in range(0, self.K):
            for i in range(0, len(self.T)):
                b = self._randomBlock()
                t = self.T[i]
                self.colidir(b, t)
                self.replicar(t)


    def colidir(self, b, t):
        MaxMatching = 0
        PosMaxMatching = -1
        if t.l > 0:
            t.l -= 1
        else:
            t.l = 0
            t.tc = 0

        for q in range(0, (t.L - b.c)):
            r = self.matching(q, t, b)
            if r >= MaxMatching:
                MaxMatching = r
                PosMaxMatching = q

            if MaxMatching > self.limiar["mi"]:
                self.ligar(PosMaxMatching, t, b)

        return

    def ligar(self, PosMaxMatching, t, b):
        for a in range(PosMaxMatching, PosMaxMatching + b.c):
            t.bitsMarcados[a] = True
            t.tl += 1
        b.bc -= 1

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

    def _randomBlock(self):
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
            G.add_edge(v[0], v[1])

        self.B = G.nodes() + G.edges()
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


class Template:
    def __init__(self, long):
        self.L = 10 # quantidade de bits
        self.tc = 1 # número de cópias
        self.tl = 0 # núemro de ligações
        self.l = long # longevidade
        self.bits = list() # cadeia binária
        self.bitsMarcados = list() # lista booleana indicando quais bits estão marcados

        for i in range(0, self.L):
            self.bits.append(randrange(2))
            self.bitsMarcados.append(False)



class Block:
    def __init__(self):
        self.c = randrange(2, 6) # quantidade de bits
        self.bc = randrange(1, 101) # número de cópias
        self.bits = list() # cadeia binária

        for i in range(0, self.c):
            self.bits.append(randrange(2))


def main():
    s1 = Soup()


main()
