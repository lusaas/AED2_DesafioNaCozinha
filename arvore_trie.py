class NoTrie:
    def __init__(self):
        # Array de 26 posições para cobrir as letras de 'a' a 'z'.
        # Iniciamos todos os caminhos como None (vazios).
        self.filhos = [None] * 26
        # Indica se uma palavra termina exatamente neste nó
        self.fim_da_palavra = False
        # Guarda uma lista de receitas que correspondem a esta palavra/frase
        self.receitas = []

class ArvoreTrie:
    def __init__(self):
        self.raiz = NoTrie()

    def _char_para_indice(self, char: str) -> int:
        """Função auxiliar para converter letras 'a'-'z' em índices 0-25."""
        # Usamos ord() para pegar o valor ASCII do caractere.
        # Exemplo: ord('a') - ord('a') = 0 | ord('b') - ord('a') = 1
        return ord(char) - ord('a')

    def _normalizar_string(self, texto: str) -> str:
        """Remove espaços e caracteres especiais básicos para indexação na Trie."""
        # Mantém apenas as letras de 'a' a 'z' em minúsculo
        texto_limpo = ""
        for char in texto.lower():
            if 'a' <= char <= 'z':
                texto_limpo += char
        return texto_limpo

    def inserir(self, nome_receita: str, receita_objeto):
        """Insere o nome da receita na árvore caractere por caractere."""
        nome_limpo = self._normalizar_string(nome_receita)
        no_atual = self.raiz

        for char in nome_limpo:
            indice = self._char_para_indice(char)
           
            # Se o caminho para essa letra não existe, criamos um novo nó
            if not no_atual.filhos[indice]:
                no_atual.filhos[indice] = NoTrie()
               
            # Caminha para o nó filho
            no_atual = no_atual.filhos[indice]

        # Ao terminar a palavra, marcamos o fim e guardamos o objeto da Receita lá
        no_atual.fim_da_palavra = True
        no_atual.receitas.append(receita_objeto)

    def buscar_por_prefixo(self, prefixo: str) -> list:
        """Busca e retorna todas as receitas que começam com o prefixo digitado."""
        prefixo_limpo = self._normalizar_string(prefixo)
        no_atual = self.raiz

        # 1. Navega até o último nó do prefixo digitado
        for char in prefixo_limpo:
            indice = self._char_para_indice(char)
            if not no_atual.filhos[indice]:
                return [] # Prefixo não encontrado na árvore
            no_atual = no_atual.filhos[indice]

        # 2. Coleta todas as receitas a partir desse nó usando uma busca em profundidade (DFS)
        resultados = []
        self._coletar_todas_da_subarvore(no_atual, resultados)
        return resultados

    def _coletar_todas_da_subarvore(self, no_atual: NoTrie, resultados: list):
        """Método recursivo (DFS) para varrer a subárvore acumulando as receitas."""
        if no_atual.fim_da_palavra:
            resultados.extend(no_atual.receitas)

        # Percorre recursivamente todos os 26 filhos possíveis do nó
        for filho in no_atual.filhos:
            if filho:
                self._coletar_todas_da_subarvore(filho, resultados)