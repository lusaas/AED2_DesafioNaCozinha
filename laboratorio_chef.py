class LaboratorioChef:
    def __init__(self, hash_sistema):
        self.hash_sistema = hash_sistema

    def _calcular_similaridade(self, r1, r2) -> int:
        """
        Calcula quantos ingredientes duas receitas compartilham em comum.
        """
        ing1 = set(r1.ingredientes)
        ing2 = set(r2.ingredientes)
        return len(ing1.intersection(ing2))

    def identificar_familias_culinarias(self, limiar_minimo: int = 2):
        """
        Descobre automaticamente comunidades/familias de receitas baseadas
        no compartilhamento de ingredientes (Grafo de Co-ocorrência).
        """
        todas_receitas = self.hash_sistema.obter_todas_receitas()
        n = len(todas_receitas)
        
        if n == 0:
            print("\nNenhuma receita cadastrada para analisar.")
            return

        # 1. Construção do Grafo de Similaridade (Lista de Adjacência)
        # Formato: {id_receita: {id_vizinho: peso_similaridade}}
        grafo = {r.id: {} for r in todas_receitas}
        
        for i in range(n):
            for j in range(i + 1, n):
                r1 = todas_receitas[i]
                r2 = todas_receitas[j]
                sim = self._calcular_similaridade(r1, r2)
                
                # Só conecta se compartilharem ao menos o limiar mínimo de ingredientes
                if sim >= limiar_minimo:
                    grafo[r1.id][r2.id] = sim
                    grafo[r2.id][r1.id] = sim

        # 2. Busca em Largura (BFS) para encontrar Componentes Conectados (Famílias)
        visitados = set()
        familias = []

        for r in todas_receitas:
            if r.id not in visitados:
                # Nova comunidade encontrada
                comunidade_atual = []
                fila = [r.id]
                visitados.add(r.id)

                while fila:
                    atual_id = fila.pop(0)
                    comunidade_atual.append(self.hash_sistema.buscar(atual_id))

                    for vizinho_id in grafo[atual_id]:
                        if vizinho_id not in visitados:
                            visitados.add(vizinho_id)
                            fila.append(vizinho_id)
                
                # Ignora pratos isolados que não se conectam a nenhum outro
                if len(comunidade_atual) > 1:
                    familias.append(comunidade_atual)

        # 3. Exibição dos Resultados (Tomada de Decisão)
        print("\n" + "="*55)
        print(f"{'LABORATÓRIO DO CHEF: COMUNIDADES GASTRONÔMICAS':^55}")
        print("="*55)
        print(f"Analisando interconexões de ingredientes entre {n} receitas...")
        print(f"Limiar de corte adotado: mínimo {limiar_minimo} ingredientes iguais.")
        print("-" * 55)

        if not familias:
            print("Nenhuma família forte detectada com o limiar atual.")
        else:
            # Ordena as comunidades pelo tamanho (maior para menor)
            familias.sort(key=len, reverse=True)
            for idx, fam in enumerate(familias, 1):
                print(f"\nFamília Culinária #{idx} ({len(fam)} pratos altamente relacionados):")
                
                # Identifica quais são os ingredientes mais comuns que unem essa família
                ingredientes_comuns = set(fam[0].ingredientes)
                for prato in fam[1:]:
                    ingredientes_comuns = ingredientes_comuns.intersection(set(prato.ingredientes))
                
                if ingredientes_comuns:
                    print(f"Ingredientes de conexão: {', '.join(list(ingredientes_comuns)[:3])}")
                
                for prato in fam[:5]:  # Mostra até 5 pratos do grupo
                    print(f"    • {prato.nome:<30} | Categoria: {prato.categoria}")
                if len(fam) > 5:
                    print(f"    • ... e mais {len(fam) - 5} pratos.")
                print("-" * 55)