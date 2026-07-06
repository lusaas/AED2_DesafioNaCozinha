from receita import Receita

class Grafo:
    def __init__(self):
        self.grafo = {}

    def adiciona(self, id_origem: int, id_destino: int):
        if id_origem not in self.grafo:
            self.grafo[id_origem] = []

        if id_destino not in self.grafo[id_origem]:
            self.grafo[id_origem].append(id_destino)

        if id_destino not in self.grafo:
            self.grafo[id_destino] = []
        
    def imprime_grafo(self):
        for n in self.grafo:
            pass
