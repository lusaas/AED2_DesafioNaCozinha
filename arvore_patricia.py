class NoPatricia:
    def __init__(self):
        
        self.filhos = {} 
        self.fim_da_palavra = False
        self.receitas = []

class ArvorePatricia:
    def __init__(self, trie_original):
        """Recebe a Trie R-way padrão e inicia o processo de compressão."""
        self.raiz = NoPatricia()
        # O nó raiz da Trie original está em trie_original.raiz
        self._comprimir_caminhos(trie_original.raiz, self.raiz)
    
    def _obter_filhos_ativos(self, no_trie):
        """Função auxiliar que diz quais os índices (0-25) que têm filhos na Trie padrão."""
        return [i for i in range(26) if no_trie.filhos[i] is not None]

    def _comprimir_caminhos(self, no_trie, no_patricia):
        """Percorre a Trie padrão e colapsa nós com um único filho."""
        for i in range(26):
            filho_trie = no_trie.filhos[i]
            if filho_trie:
                # Transforma o índice (0-25) de volta na letra (a-z)
                fragmento = chr(i + ord('a'))
                no_atual = filho_trie
                
                filhos_ativos = self._obter_filhos_ativos(no_atual)
                
                # O SEGREDO DA COMPRESSÃO:
                # Enquanto tiver exatamente 1 filho e NÃO for o fim de uma receita, colapsamos!
                while len(filhos_ativos) == 1 and not no_atual.fim_da_palavra:
                    unico_indice = filhos_ativos[0]
                    fragmento += chr(unico_indice + ord('a')) # Adiciona a próxima letra
                    no_atual = no_atual.filhos[unico_indice]  # Avança na Trie antiga
                    filhos_ativos = self._obter_filhos_ativos(no_atual)
                
                # Criamos o nó final comprimido
                novo_no_patricia = NoPatricia()
                novo_no_patricia.fim_da_palavra = no_atual.fim_da_palavra
                novo_no_patricia.receitas = no_atual.receitas
                
                # Ligamos o fragmento (ex: "utor") ao novo nó
                no_patricia.filhos[fragmento] = novo_no_patricia
                
                # Continuamos a recursão para os filhos caso existam ramificações a partir daqui
                self._comprimir_caminhos(no_atual, novo_no_patricia)

    # ==========================================
    #         IMPRESSÃO VISUAL DA ÁRVORE
    # ==========================================
    def imprimir_arvore(self, no=None, nivel=0):
        """Desenha a árvore no terminal para provar a compressão."""
        if no is None:
            no = self.raiz
            print("\n" + "="*50)
            print(f"{'ÁRVORE PATRICIA (COMPRIMIDA)':^50}")
            print("="*50)
            if not no.filhos:
                print("(Árvore vazia)")
                return

        for fragmento, filho in no.filhos.items():
            marca = " [FIM_DA_RECEITA]" if filho.fim_da_palavra else ""
            print("    " * nivel + f"|-- '{fragmento}'{marca}")
            self.imprimir_arvore(filho, nivel + 1)

    # ==========================================
    #        BUSCA POR PREFIXO ADAPTADA
    # ==========================================
    def buscar_por_prefixo(self, prefixo: str) -> list:
        """Busca receitas suportando a nova estrutura de dicionário."""
        prefixo_limpo = prefixo.lower().replace(" ", "")
        return self._buscar_recursivo(self.raiz, prefixo_limpo)
        
    def _buscar_recursivo(self, no, prefixo_restante):
        # Se esgotamos o prefixo digitado, recolhemos todas as receitas a partir daqui
        if not prefixo_restante:
            return self._coletar_todas(no)
            
        for fragmento, filho in no.filhos.items():
            # Caso 1: O fragmento tem o prefixo dentro dele. (Ex: procuro "au", e o nó tem "autor")
            if fragmento.startswith(prefixo_restante):
                return self._coletar_todas(filho)
                
            # Caso 2: O prefixo é maior que o fragmento. (Ex: procuro "autor", e o nó tem "au")
            elif prefixo_restante.startswith(fragmento):
                novo_prefixo = prefixo_restante[len(fragmento):]
                return self._buscar_recursivo(filho, novo_prefixo)
                
        return [] # Não encontrou nada

    def _coletar_todas(self, no) -> list:
        """DFS para recolher receitas dos nós filhos."""
        resultados = []
        if no.fim_da_palavra:
            resultados.extend(no.receitas)
        for filho in no.filhos.values():
            resultados.extend(self._coletar_todas(filho))
        return resultados