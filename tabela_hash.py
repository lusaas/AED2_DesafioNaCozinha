class NoHash:
    
    def __init__(self, chave: int, valor, proximo=None):
        self.chave = chave       # Será o ID da receita
        self.valor = valor       # Será o objeto da Receita
        self.proximo = proximo   # Ponteiro para o próximo nó em caso de colisão

class TabelaHash:
    def __init__(self, capacidade: int = 23):
        # número primo para a capacidade inicial (ajuda a evitar colisões)
        self.capacidade = capacidade
        self.tabela = [None] * self.capacidade
        self.total_itens = 0

    def _funcao_hash(self, chave: int) -> int:
        #Método da Divisão para calcular o índice na tabela.
        return chave % self.capacidade

    def calcular_assinatura_receita(self, receita) -> str:
        #Gera um identificador único  baseado no conteúdo da receita.
        ingredientes_ordenados = sorted(receita.ingredientes)
        conteudo_bruto = f"{receita.nome}|{receita.categoria}|{receita.tempo_preparo}|{receita.custo}|{','.join(ingredientes_ordenados)}"
       
        # Algoritmo simples de hash de string  para gerar a assinatura sem imports externos
        hash_calculado = 5381
        for char in conteudo_bruto:
            hash_calculado = ((hash_calculado << 5) + hash_calculado) + ord(char)
       
        # Retorna em formato hexadecimal string fixa
        return hex(hash_calculado & 0xFFFFFFFF)

    def inserir(self, chave: int, valor):
        #Insere uma receita na tabela. Se o ID já existir, atualiza o valor.
        if not hasattr(valor, 'assinatura_original') or valor.assinatura_original is None:
            valor.assinatura_original = self.calcular_assinatura_receita(valor)

        indice = self._funcao_hash(chave)
        no_atual = self.tabela[indice]

        # Navega pela lista encadeada daquela posição para checar se a chave já existe
        while no_atual:
            if no_atual.chave == chave:
                no_atual.valor = valor # Atualiza se já existir
                return
            no_atual = no_atual.proximo

        # Se não existia, insere no INÍCIO da lista encadeada
        novo_no = NoHash(chave, valor, self.tabela[indice])
        self.tabela[indice] = novo_no
        self.total_itens += 1

    def buscar(self, chave: int):
        #Busca uma receita pelo ID em tempo médio O(1).
        indice = self._funcao_hash(chave)
        no_atual = self.tabela[indice]

        while no_atual:
            if no_atual.chave == chave:
                return no_atual.valor
            no_atual = no_atual.proximo
        return None
    def buscar_por_ingrediente(self, ingrediente_busca: str) -> list:
        """
        Varre toda a tabela hash procurando por receitas que contenham 
        o ingrediente especificado.
        """
        resultados = []
        # Normaliza o termo de busca para evitar problemas com maiúsculas/minúsculas
        termo_limpo = ingrediente_busca.strip().lower()

        # Percorre todas as posições do array da tabela
        for indice in range(self.capacidade):
            no_atual = self.tabela[indice]
            
            # Percorre a lista encadeada (tratamento de colisão) daquela posição
            while no_atual:
                receita = no_atual.valor
                # Verifica se o ingrediente está na lista da receita
                if termo_limpo in receita.ingredientes:
                    resultados.append(receita)
                
                no_atual = no_atual.proximo

        return resultados
    
            # MODO INVESTIGAÇÃO (SABOTAGENS)
    
    def investigar_sabotagens(self) -> list:
        #Percorre toda a tabela verificando se alguma receita foi modificada ilegalmente.
        receitas_corrompidas = []

        # Varre todas as posições do array da tabela
        for indice in range(self.capacidade):
            no_atual = self.tabela[indice]
           
            # Varre a lista encadeada daquela posição
            while no_atual:
                receita = no_atual.valor
                # Calcula a assinatura com o conteúdo ATUAL da memória
                assinatura_atual = self.calcular_assinatura_receita(receita)
               
                # Se o conteúdo atual divergir do carimbo original de inserção, houve sabotagem!
                if assinatura_atual != receita.assinatura_original:
                    receitas_corrompidas.append(receita)
               
                no_atual = no_atual.proximo

        return list(set(receitas_corrompidas)) # Remove duplicados de referência se houver