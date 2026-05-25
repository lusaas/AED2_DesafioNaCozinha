class NoTrie:
    def __init__(self):
        self.filhos = [None] * 26
        self.fim_da_palavra = False
        self.receitas = []

class ArvoreTrie:
    def __init__(self):
        self.raiz = NoTrie()

    def _char_para_indice(self, char: str) -> int:
        
        return ord(char) - ord('a')

    def _normalizar_string(self, texto: str) -> str:
       
        texto_limpo = ""
        for char in texto.lower():
            if 'a' <= char <= 'z':
                texto_limpo += char
        return texto_limpo

    def inserir(self, nome_receita: str, receita_objeto):
        nome_limpo = self._normalizar_string(nome_receita)
        no_atual = self.raiz

        for char in nome_limpo:
            indice = self._char_para_indice(char)
           
            if not no_atual.filhos[indice]:
                no_atual.filhos[indice] = NoTrie()
               
            no_atual = no_atual.filhos[indice]

        no_atual.fim_da_palavra = True
        no_atual.receitas.append(receita_objeto)

    def buscar_por_prefixo(self, prefixo: str) -> list:
       
        prefixo_limpo = self._normalizar_string(prefixo)
        no_atual = self.raiz

        for char in prefixo_limpo:
            indice = self._char_para_indice(char)
            if not no_atual.filhos[indice]:
                return [] # Prefixo não encontrado na árvore
            no_atual = no_atual.filhos[indice]

        resultados = []
        self._coletar_todas_da_subarvore(no_atual, resultados)
        return resultados

    def _coletar_todas_da_subarvore(self, no_atual: NoTrie, resultados: list):
        
        if no_atual.fim_da_palavra:
            resultados.extend(no_atual.receitas)

        for filho in no_atual.filhos:
            if filho:
                self._coletar_todas_da_subarvore(filho, resultados)