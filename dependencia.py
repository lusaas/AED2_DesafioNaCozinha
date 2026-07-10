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
        
    def imprime_grafo(self, hash_sistema):
        print("\n" + "="*55)
        print(f"{'FLUXO DE DEPENDÊNCIAS DIRETA'::^55}")
        print("="*55)

        tem_dependencia = False

        for id_origem, destinos in self.grafo.items():
            if destinos:
                tem_dependencia = True

                r_origem = hash_sistema.buscar(id_origem)
                nome_origem = r_origem.nome if r_origem else f"ID {id_origem}"

                for id_destino in destinos:
                    r_destino = hash_sistema.buscar(id_destino)
                    nome_destino = r_destino.nome if r_destino else f"ID {id_destino}"

                    print(f"{nome_origem} -> {nome_destino}")

        if not tem_dependencia:
            print(f"{'Nenhuma dependência cadastrada no sistema.':^55}")

        print("="*55)
        return
    
    def identificar_inconsistencias(self, hash_sistema) -> bool:
        estados = {no: 0 for no in self.grafo}
        ciclos_encontrados = []

        def dfs_detecta_ciclo(no_atual, caminho_atual):
            estados[no_atual] = 1
            caminho_atual.append(no_atual)

            for vizinho in self.grafo.get(no_atual, []):
                if estados.get(vizinho, 0) == 1:
                    indice_inicio = caminho_atual.index(vizinho)
                    ciclo_completo = caminho_atual[indice_inicio:] + [vizinho]
                    ciclos_encontrados.append(ciclo_completo)
                elif estados.get(vizinho, 0) == 0:
                    dfs_detecta_ciclo(vizinho, caminho_atual)

            estados[no_atual] = 2
            caminho_atual.pop()

        for no in self.grafo:
            if estados[no] == 0:
                dfs_detecta_ciclo(no, [])

        print("\n" + "="*55)
        print(f"{'VARREDURA DE CONSISTÊNCIA DO GRAFO':^55}")
        print("="*55)

        if ciclos_encontrados:
            print(f"Alerta: Detectadas{len(ciclos_encontrados)} ciclos!")
            print("O fluxo de preparo está travado nos seguintes loops:\n")
            
            for ciclo in ciclos_encontrados:
                nomes_ciclo = []
                for id_node in ciclo:
                    r = hash_sistema.buscar(id_node)
                    nomes_ciclo.append(r.nome if r else f"ID {id_node}")
                
                print("  --> " + " -> ".join(nomes_ciclo))
            return True
        else:
            print("Grafo Consistente!")
            return False
        
    def ordenar(self, hash_sistema):
        estados = {no: 0 for no in self.grafo}
        pilha_sequencia = []
        ciclo_detectado = [False]

        def dfs_topologica(no_atual):
            if ciclo_detectado[0]:
                return
            
            estados[no_atual] = 1

            for vizinho in self.grafo.get(no_atual, []):
                if estados.get(vizinho, 0) == 1:
                    ciclo_detectado[0] = True
                    return
                elif estados.get(vizinho, 0) == 0:
                    dfs_topologica(vizinho)

            estados[no_atual] = 2
            pilha_sequencia.insert(0, no_atual)

        for no in self.grafo:
            if estados[no] == 0:
                dfs_topologica(no)

        print("\n" + "="*55)
        print(f"{'Preparo ideal':^55}")
        print("="*55)

        if ciclo_detectado[0]:
            print("Impossível gerar ordenação")
            print("="*55)
            return False
        
        for i, id_receita in enumerate(pilha_sequencia, 1):
            r = hash_sistema.buscar(id_receita)
            nome_receita = r.nome if r else f"Componente Base (ID {id_receita})"

            if i < len(pilha_sequencia):
                print(f"  {i}º: {nome_receita} \n        ▼")
            else:
                print(f"  {i}º: {nome_receita} (Conclusão do Fluxo)")

        print("="*55)
        return True