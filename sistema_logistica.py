import collections

class Vertice:
    def __init__(self, id_ponto: str, tipo: str, capacidade_processo: int = 9999):
        """
        tipo: 'cozinha', 'hub' (ponto de retirada) ou 'regiao' (regiao de entrega)
        """
        self.id = id_ponto
        self.tipo = tipo
        self.capacidade_processo = capacidade_processo  # Restrição física do nó
        self.adjacentes = {}  # Conexões: {Vertice_Destino: Aresta}

class Aresta:
    def __init__(self, origem: str, destino: str, tempo: float, capacidade: int):
        self.origem = origem
        self.destino = destino
        self.tempo = tempo            # Peso para caminho mais rápido (Dijkstra)
        self.capacidade = capacidade  # Limite de vazão de pedidos (Fluxo Máximo)
        self.fluxo = 0                # Usado no cálculo de fluxo máximo

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

    # --- ALGORITMO 1: DIJKSTRA (Rotas e Tempos Operacionais) ---
    def calcular_rota_mais_rapida(self, origem: str, destino: str):
        """
        Calcula o caminho com o menor tempo operacional de um ponto a outro.
        """
        # Validação inicial de existência dos pontos
        if origem not in self.vertices or destino not in self.vertices:
            return None, float('inf')

        # Dicionários indexados estritamente pelas chaves de string (IDs dos vértices)
        distancias = {v_id: float('inf') for v_id in self.vertices}
        predecessores = {v_id: None for v_id in self.vertices}
        distancias[origem] = 0
        
        nao_visitados = list(self.vertices.keys())

        while nao_visitados:
            # Encontra o ID de vértice não visitado com a menor distância acumulada
            atual = min(nao_visitados, key=lambda v: distancias[v])
            nao_visitados.remove(atual)

            # Se a menor distância for infinito, os pontos restantes estão desconectados
            if distancias[atual] == float('inf'):
                break

            # Se chegamos ao destino, podemos encerrar a busca antecipadamente
            if atual == destino:
                break

            vertice_atual = self.vertices[atual]
            # Explora cada um dos vizinhos conectados diretamente ao vértice atual
            for vizinho_obj, aresta in vertice_atual.adjacentes.items():
                vizinho_id = vizinho_obj.id
                if vizinho_id in nao_visitados:
                    novo_tempo = distancias[atual] + aresta.tempo
                    if novo_tempo < distancias[vizinho_id]:
                        distancias[vizinho_id] = novo_tempo
                        predecessores[vizinho_id] = atual

        # Reconstrói o caminho de trás para frente a partir do destino
        caminho = []
        passo = destino
        while passo is not None:
            caminho.insert(0, passo)
            passo = predecessores[passo]

        # Se o primeiro elemento não for a origem, significa que o destino é inacessível
        if not caminho or caminho[0] != origem:
            return [], float('inf')
            
        return caminho, distancias[destino]

    # --- ALGORITMO 2: EDMONDS-KARP / FORD-FULKERSON (Capacidade Máxima e Gargalos) ---
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
        """
        Determina a quantidade máxima de entregas que podem ser processadas simultaneamente
        e aponta onde estão os gargalos do sistema (arestas operando em capacidade máxima).
        """
        # Reseta os fluxos de todas as arestas do grafo
        for v in self.vertices.values():
            for aresta in v.adjacentes.values():
                aresta.fluxo = 0

        pai = {}
        fluxo_maximo = 0

        while self._bfs_caminho_aumentante(super_fonte, super_sumidouro, pai):
            # Encontra o gargalo do caminho aumentante atual
            fluxo_caminho = float('inf')
            s = super_sumidouro
            while s != super_fonte:
                u = pai[s]
                aresta = self.vertices[u].adjacentes[self.vertices[s]]
                fluxo_caminho = min(fluxo_caminho, aresta.capacidade - aresta.fluxo)
                s = u

            # Atualiza os fluxos nas arestas
            v = super_sumidouro
            while v != super_fonte:
                u = pai[v]
                self.vertices[u].adjacentes[self.vertices[v]].fluxo += fluxo_caminho
                v = u

            fluxo_maximo += fluxo_caminho

        # Identifica os gargalos (rotas que estão operando em 100% da sua capacidade limite)
        gargalos = []
        for v in self.vertices.values():
            for aresta in v.adjacentes.values():
                if aresta.capacidade > 0 and aresta.fluxo == aresta.capacidade:
                    gargalos.append((aresta.origem, aresta.destino, aresta.capacidade))

        return fluxo_maximo, gargalos