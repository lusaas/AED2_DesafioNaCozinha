class ModuloChef:
    def __init__(self, lista_receitas: list):
        # Recebe a lista de receitas carregadas no sistema
        self.receitas = lista_receitas

    def _merge_sort_custo(self, lista: list) -> list:
        """Implementação manual do MergeSort para ordenar por custo (crescente)."""
        if len(lista) <= 1:
            return list(lista) # Copia a lista se tiver 1 elemento ou menos

        meio = len(lista) // 2
        esquerda = self._merge_sort_custo(lista[:meio])
        direita = self._merge_sort_custo(lista[meio:])

        return self._merge(esquerda, direita)

    def _merge(self, esquerda: list, direita: list) -> list:
        resultado = []
        i = j = 0

        while i < len(esquerda) and j < len(direita):
            # Critério de ordenação: Menor Custo Primeiro
            if esquerda[i].custo <= direita[j].custo:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1

        # Adiciona o restante dos elementos que sobraram
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        return resultado

    # ==================================================
    # ALGORITMO GULOSO: RECOMENDAÇÃO DE MENU ECONÔMICO
    # ==================================================
    def gerar_menu_economico(self, orcamento_maximo: float) -> tuple:
        """
        Algoritmo Guloso para maximizar a quantidade de pratos dentro de um orçamento.
        Estratégia: Escolhe sempre a receita mais barata disponível no momento.
        """
        # 1. Escolha Gulosa: Ordena manualmente todas as receitas pelo menor custo
        receitas_ordenadas = self._merge_sort_custo(self.receitas)

        menu_sugerido = []
        custo_total = 0.0

        # 2. Passo Guloso: Vai pegando os itens mais baratos até o orçamento estourar
        for receita in receitas_ordenadas:
            if custo_total + receita.custo <= orcamento_maximo:
                menu_sugerido.append(receita)
                custo_total += receita.custo
            else:
                # Como a lista está ordenada por custo, se o atual não cabe,
                # nenhum dos próximos mais caros caberá. Podemos parar.
                break

        return menu_sugerido, round(custo_total, 2)