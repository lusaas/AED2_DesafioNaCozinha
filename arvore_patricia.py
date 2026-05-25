class NoPatricia:
    def __init__(self):
        
        self.filhos = {} 
        self.fim_da_palavra = False
        self.receitas = []

class ArvorePatricia:
    def __init__(self, trie_original):
       
        self.raiz = NoPatricia()
        self._comprimir_caminhos(trie_original.raiz, self.raiz)

    def _obter_filhos_ativos(self, no_trie):
       
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
                
                
                # Enquanto tiver exatamente 1 filho e NÃO for o fim de uma receita, colapsamos!
                while len(filhos_ativos) == 1 and not no_atual.fim_da_palavra:
                    unico_indice = filhos_ativos[0]
                    fragmento += chr(unico_indice + ord('a')) # Adiciona a próxima letra
                    no_atual = no_atual.filhos[unico_indice]  # Avança na Trie antiga
                    filhos_ativos = self._obter_filhos_ativos(no_atual)
                
               
                novo_no_patricia = NoPatricia()
                novo_no_patricia.fim_da_palavra = no_atual.fim_da_palavra
                novo_no_patricia.receitas = no_atual.receitas
                
               
                no_patricia.filhos[fragmento] = novo_no_patricia
                
                
                self._comprimir_caminhos(no_atual, novo_no_patricia)

    # ==========================================
    #         IMPRESSÃO VISUAL DA ÁRVORE
    # ==========================================
    def imprimir_arvore(self, no=None, nivel=0):
        
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
        
        prefixo_limpo = prefixo.lower().replace(" ", "")
        return self._buscar_recursivo(self.raiz, prefixo_limpo)
        
    def _buscar_recursivo(self, no, prefixo_restante):
        # Se esgotamos o prefixo digitado, recolhemos todas as receitas a partir daqui
        if not prefixo_restante:
            return self._coletar_todas(no)
            
        for fragmento, filho in no.filhos.items():
            # Caso 1: O fragmento tem o prefixo dentro dele.
            if fragmento.startswith(prefixo_restante):
                return self._coletar_todas(filho)
                
            # Caso 2: O prefixo é maior que o fragmento.
            elif prefixo_restante.startswith(fragmento):
                novo_prefixo = prefixo_restante[len(fragmento):]
                return self._buscar_recursivo(filho, novo_prefixo)
                
        return [] # Não encontrou nada

    def _coletar_todas(self, no) -> list:
       
        resultados = []
        if no.fim_da_palavra:
            resultados.extend(no.receitas)
        for filho in no.filhos.values():
            resultados.extend(self._coletar_todas(filho))
        return resultados