# -*- coding: utf-8 -*-
import pandas as pd
from random import randrange

class Soup:
    def __init__(self):
        self.K = 10000 # total de colisões
        self.limiar = {
            "lambda": 9, # limiar de replicação => qtd mínima de bits para replicar
            "mi": 2 # limiar de matching => qtd mínima de bits para ligar um bloco e um template
        }
        self.bl = 100 # bonificação de longevidade
        self.pm = 0.01 # probabilidade de mutação
        self.m = 0.001# número gaussiano aleatório
        self.T = list()
        self.B = list()

        self._inicializa(4, 1000)
        
        lista = list()

        for k in range(0, self.K):
            # print("\n************************Colisão K =", k ,"********************************\n")
            obj = dict()
            for i in range(0, len(self.T)):
                # print("\t\t[[TEMPLATE T =", i, "]]\n")
                b = self._randomBlock()
                t = self.T[i]
                # print("Template antes:")
                # print(t.bits)
                # print("Num cópias: " + str(t.tc) + " Num ligações: " + str(t.tl) + " Num longevidade: " + str(t.l))
                self.colidir(b, t)
                self.replicar(t)
                
                obj["tc" + str(i)] = t.tc
                
                # print("\nTemplate depois:")
                # print(t.bits)
                # print("Num cópias: " + str(t.tc) + " Num ligações: " + str(t.tl) + " Num longevidade: " + str(t.l))
                # print("\n---------------------------------------------------------------------------\n")
            # print("\n************************************************************************\n")
            lista.append(obj)
        
        
        global graph1
        graph1 = pd.DataFrame(data = lista, columns=["tc0", "tc1", "tc2", "tc3"])

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

    # Inicializa os conjuntos de blocos e templates.
    # Params:
    #   nt => número de templates
    #   nb => número de blocos construtivos
    def _inicializa(self, nt, nb):
        for i in range(0, nt):
            l = self.K * 0.10
            t = Template(l)
            self.T.append(t)

        for j in range(0, nb):
            b = Block()
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