class ModuloChef:
    def __init__(self, lista_receitas: list):
        # Recebe a lista de receitas carregadas no sistema
        self.receitas = lista_receitas

    def _merge_sort_custo(self, lista: list) -> list:
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

        
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        return resultado
    
    def gerar_menu_economico(self, orcamento_maximo: float) -> tuple:
        
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
                break

        return menu_sugerido, round(custo_total, 2)