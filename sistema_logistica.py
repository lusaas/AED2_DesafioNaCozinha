import collections

class Vertice:
    def __init__(self, id_ponto: str, tipo: str, capacidade_processo: int = 9999):
        self.id = id_ponto
        self.tipo = tipo
        self.capacidade_processo = capacidade_processo
        self.adjacentes = {}

class Aresta:
    def __init__(self, origem: str, destino: str, tempo: float, capacidade: int):
        self.origem = origem
        self.destino = destino
        self.tempo = tempo            
        self.capacidade = capacidade 
        self.fluxo = 0  

class GrafoLogistica:
    def __init__(self):
        self.vertices = {}

    def adicionar_vertice(self, id_ponto: str, tipo: str, capacidade: int = 9999):
        if id_ponto not in self.vertices:
            self.vertices[id_ponto] = Vertice(id_ponto, tipo, capacidade)

    def adicionar_conexao(self, origem: str, destino: str, tempo: float, capacidade: int):
        if origem in self.vertices and destino in self.vertices:
            aresta = Aresta(origem, destino, tempo, capacidade=capacidade)
            self.vertices[origem].adjacentes[self.vertices[destino]] = aresta

    def calcular_rota_mais_rapida(self, origem: str, destino: str):
        if origem not in self.vertices or destino not in self.vertices:
            return None, float('inf')

        distancias = {v_id: float('inf') for v_id in self.vertices}
        predecessores = {v_id: None for v_id in self.vertices}
        distancias[origem] = 0
        
        nao_visitados = list(self.vertices.keys())

        while nao_visitados:
            atual = min(nao_visitados, key=lambda v: distancias[v])
            nao_visitados.remove(atual)

            if distancias[atual] == float('inf'):
                break

            if atual == destino:
                break

            vertice_atual = self.vertices[atual]
            for vizinho_obj, aresta in vertice_atual.adjacentes.items():
                vizinho_id = vizinho_obj.id
                if vizinho_id in nao_visitados:
                    novo_tempo = distancias[atual] + aresta.tempo
                    if novo_tempo < distancias[vizinho_id]:
                        distancias[vizinho_id] = novo_tempo
                        predecessores[vizinho_id] = atual

        caminho = []
        passo = destino
        while passo is not None:
            caminho.insert(0, passo)
            passo = predecessores[passo]

        if not caminho or caminho[0] != origem:
            return [], float('inf')
            
        return caminho, distancias[destino]

    def _bfs_caminho_aumentante(self, s: str, t: str, pai: dict) -> bool:
        visitados = {v: False for v in self.vertices}
        fila = collections.deque([s])
        visitados[s] = True

        while fila:
            u = fila.popleft()
            vertice_u = self.vertices[u]

            for vizinho, aresta in vertice_u.adjacentes.items():
                v = vizinho.id
                capacidade_residual = aresta.capacidade - aresta.fluxo
                if not visitados[v] and capacidade_residual > 0:
                    fila.append(v)
                    visitados[v] = True
                    pai[v] = u
                    if v == t:
                        return True
        return False

    def calcular_capacidade_maxima(self, super_fonte: str, super_sumidouro: str):
        for v in self.vertices.values():
            for aresta in v.adjacentes.values():
                aresta.fluxo = 0

        pai = {}
        fluxo_maximo = 0

        while self._bfs_caminho_aumentante(super_fonte, super_sumidouro, pai):
            fluxo_caminho = float('inf')
            s = super_sumidouro
            while s != super_fonte:
                u = pai[s]
                aresta = self.vertices[u].adjacentes[self.vertices[s]]
                fluxo_caminho = min(fluxo_caminho, aresta.capacidade - aresta.fluxo)
                s = u

            v = super_sumidouro
            while v != super_fonte:
                u = pai[v]
                self.vertices[u].adjacentes[self.vertices[v]].fluxo += fluxo_caminho
                v = u

            fluxo_maximo += fluxo_caminho

        gargalos = []
        for v in self.vertices.values():
            for aresta in v.adjacentes.values():
                if aresta.capacidade > 0 and aresta.fluxo == aresta.capacidade:
                    gargalos.append((aresta.origem, aresta.destino, aresta.capacidade))

        return fluxo_maximo, gargalos