class LaboratorioChef:
    def __init__(self, hash_sistema):
        self.hash_sistema = hash_sistema

    def _calcular_similaridade(self, r1, r2) -> int:
        ing1 = set(r1.ingredientes)
        ing2 = set(r2.ingredientes)
        return len(ing1.intersection(ing2))

    def identificar_familias_culinarias(self, limiar_minimo: int = 2):
        todas_receitas = self.hash_sistema.obter_todas_receitas()
        n = len(todas_receitas)
        
        if n == 0:
            print("\nNenhuma receita cadastrada para analisar.")
            return

        grafo = {r.id: {} for r in todas_receitas}
        
        for i in range(n):
            for j in range(i + 1, n):
                r1 = todas_receitas[i]
                r2 = todas_receitas[j]
                sim = self._calcular_similaridade(r1, r2)
                
                if sim >= limiar_minimo:
                    grafo[r1.id][r2.id] = sim
                    grafo[r2.id][r1.id] = sim

        visitados = set()
        familias = []

        for r in todas_receitas:
            if r.id not in visitados:
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
                
                if len(comunidade_atual) > 1:
                    familias.append(comunidade_atual)

        print("\n" + "="*55)
        print(f"{'LABORATÓRIO DO CHEF: COMUNIDADES GASTRONÔMICAS':^55}")
        print("="*55)
        print(f"Analisando interconexões de ingredientes entre {n} receitas")
        print(f"Limiar de corte adotado: mínimo {limiar_minimo} ingredientes iguais.")
        print("-" * 55)

        if not familias:
            print("Nenhuma família forte detectada com o limiar atual.")
        else:
            familias.sort(key=len, reverse=True)
            for idx, fam in enumerate(familias, 1):
                print(f"\nFamília Culinária #{idx} ({len(fam)} pratos altamente relacionados):")
                
                ingredientes_comuns = set(fam[0].ingredientes)
                for prato in fam[1:]:
                    ingredientes_comuns = ingredientes_comuns.intersection(set(prato.ingredientes))
                
                if ingredientes_comuns:
                    print(f"Ingredientes de conexão: {', '.join(list(ingredientes_comuns)[:3])}")
                
                for prato in fam[:5]:
                    print(f"    • {prato.nome:<30} | Categoria: {prato.categoria}")
                if len(fam) > 5:
                    print(f"    • ... e mais {len(fam) - 5} pratos.")
                print("-" * 55)