# -*- coding: utf-8 -*-
import pandas as pd
import networkx as NX
from random import randrange

class Soup:
    def __init__(self, fileName, K):
        # lambda => limiar de replicação (min de bits p/ replicar);
        # mi => limiar de matching (min de bits p/ ligar)
        self.limiar = { "lambda": 9, "mi": 2}
        self.K = K # total de colisões
        self.bl = 100 # bonificação de longevidade
        self.pm = 0.01 # probabilidade de mutação
        self.m = 0.001 # número gaussiano aleatório
        self.G = NX.Graph()
        self.B = list()

        self._inicializa(fileName)

        print("Antes da colisão")
        print("Len B =", len(self.B))
        print("B = [")
        for b in self.B:
            print("Cópias", b.get_copies(), b.get_value())
        print("]")
        print("------------------------------\n")

        for k in range(0, self.K):
            len_B = len(self.B)
            exception = list()

            for i in range(0, len_B):
                b1 = None
                try:
                    b1 = self.B[i]
                except Exception as e:
                    print("erro de indexação. Valor de i:", i)
                    break

                # TODO modificar as colisões de forma que todas os novos descentes
                # sejam mantidos em algum lugar até que todas as colisões presentes
                # tenham ocorrido. Só após o fim das colisões colocar os novos blocos
                # no conjunto de todos o blocos.
    

                b2 = self._randomBlock(b1, exception)
                if (b1.get_copies() and b2.get_copies()):
                    self.colidir(b1, b2)
                    exception.extend((b1,b2))
                else:
                    if (not b1.get_copies()):
                        self.elimina_bloco(b1)

                    if (not b2.get_copies()):
                        self.elimina_bloco(b2)


            print("Colisão K =", k)
            print("Len B =", len(self.B))
            print("B = [")
            for b in self.B:
                print("Cópias", b.get_copies(), b.get_value())
            print("]")
            print("------------------------------\n")
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
                if self._compare(vl_b1[i], vl_b2[j]):
                    print("replicar:", vl_b1, "e", vl_b2)
                    self.replicar(b1, i, b2, j)
                    break

        return
    #END COLIDIR


    def replicar(self, b1, idx1, b2, idx2):
        vl_n = list()
        vl_b1 = b1.get_value()
        if type(vl_b1) == type(""):
            vl_b1 = (vl_b1,)

        vl_b2 = b2.get_value()
        if type(vl_b2) == type(""):
            vl_b2 = (vl_b2,)

        if idx1 == 0:
            vl_b1 = vl_b1[::-1]

        if idx2 != 0:
            vl_b2 = vl_b2[::-1] #concatena os vertices de b1 com os vertices (na ordem inversa) de b2

        vl_n += vl_b1 + vl_b2
        vl_n = tuple(vl_n)

        b_n = self.existe_bloco(vl_n)

        if b_n == False :
            b_n = Bloco(vl_n, 1)
            self.B.append(b_n)
            print("Bloco resultado:\n", b_n.get_value())
        else:
            b_n.increase_copies()

        b1.decrease_copies()
        b2.decrease_copies()

        if (not b1.get_copies()):
            self.elimina_bloco(b1)

        if (not b2.get_copies()):
            self.elimina_bloco(b2)

        return

    def mutar(self, t):
        PosMut = randrange(t.L)
        t.bits[PosMut] = self.xnor(t.bits[PosMut], 0)

    def elimina_bloco(self, block):
        v_block = block.get_value()
        for b in self.B:
            v_b = b.get_value()
            if v_block == v_b or v_block[::-1] == v_b:
                self.B.remove(b)
                return
        return

    def _randomBlock(self, b, exception = list()):
        j = randrange(len(self.B))

        while (self.B[j] in exception) or (self.B[j] == b):
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

    def existe_bloco (self, vl):
        self.B
        for b in self.B:
            v_b = b.get_value()
            if vl == v_b or vl == v_b[::-1]:
                return b

        return False


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
    def __init__(self, vertices, numCopies = randrange(1, 6)):
        self.copies = numCopies # número de cópias
        self.value = vertices # lista de vértices

    def get_copies(self):
        return self.copies

    def get_value(self):
        return self.value

    def decrease_copies(self):
        if self.copies > 0:
            self.copies -= 1
        return self.copies

    def increase_copies(self):
        self.copies += 1
        return self.copies
