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
    #END _INIT_


    def colidir(self, b1, b2):
        vl_b1 = b1.get_value()
        if type(vl_b1) == type(""):
            vl_b1 = [vl_b1]

        vl_b2 = b2.get_value()
        if type(vl_b2) == type(""):
            vl_b2 = [vl_b2]

        for i in [0, len(vl_b1) - 1]:
            for j in [0, len(vl_b2) - 1]:
                if _compare(vl_b1[i], vl_b2[j]):
                    self.replicar(b1, i, b2, j)

        return
    #END COLIDIR


    def replicar(self, b1, idx1, b2, idx2):
        # TODO: verificar se já não existe
        # algum bloco igual ao resultado da
        # junção destes dois, caso exista,
        # apenas aumentar o número de cópias,
        # senão, criar um novo bloco e
        # inserí-lo ao universo de blocos

        # TODO [2]: decrementar o número de
        # cópias dos blocos originais

        # TODO [3]: tentar encaixar a função
        # de mutação da nova espécie.


        return

    def mutar(self, t):
        PosMut = randrange(t.L)
        t.bits[PosMut] = self.xnor(t.bits[PosMut], 0)

    def _randomBlock(self, exception):
        j = randrange(len(self.B))

        while exception == self.B[j]:
            j = randrange(len(self.B))

        return self.B[j]

    def _compare(self, node1, node2):
        edges = self.G.edges()

        for e in edges:
            if e[0] == node1 or e[0] == node2:
                if e[1] == node1 or e[1] == node2:
                    return True

        return False

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

    def decrease_copies(self):
        if self.copies > 0:
            self.copies -= 1
        return self.copies
