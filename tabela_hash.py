class NoHash:
    
    def __init__(self, chave: int, valor, proximo=None):
        self.chave = chave
        self.valor = valor
        self.proximo = proximo

class TabelaHash:
    def __init__(self, capacidade: int = 23):
        self.capacidade = capacidade
        self.tabela = [None] * self.capacidade
        self.total_itens = 0

    def _funcao_hash(self, chave: int) -> int:
        return chave % self.capacidade

    def calcular_assinatura_receita(self, receita) -> str:
        ingredientes_ordenados = sorted(receita.ingredientes)
        conteudo_bruto = f"{receita.nome}|{receita.categoria}|{receita.tempo_preparo}|{receita.custo}|{','.join(ingredientes_ordenados)}"
       
        hash_calculado = 5381
        for char in conteudo_bruto:
            hash_calculado = ((hash_calculado << 5) + hash_calculado) + ord(char)
       
        return hex(hash_calculado & 0xFFFFFFFF)

    def inserir(self, chave: int, valor):
        if not hasattr(valor, 'assinatura_original') or valor.assinatura_original is None:
            valor.assinatura_original = self.calcular_assinatura_receita(valor)

        indice = self._funcao_hash(chave)
        no_atual = self.tabela[indice]

        while no_atual:
            if no_atual.chave == chave:
                no_atual.valor = valor
                return
            no_atual = no_atual.proximo

        novo_no = NoHash(chave, valor, self.tabela[indice])
        self.tabela[indice] = novo_no
        self.total_itens += 1

    def buscar(self, chave: int):
        indice = self._funcao_hash(chave)
        no_atual = self.tabela[indice]

        while no_atual:
            if no_atual.chave == chave:
                return no_atual.valor
            no_atual = no_atual.proximo
        return None
    def buscar_por_ingrediente(self, ingrediente_busca: str) -> list:
    
        resultados = []
        termo_limpo = ingrediente_busca.strip().lower()

        for indice in range(self.capacidade):
            no_atual = self.tabela[indice]
            
            while no_atual:
                receita = no_atual.valor
                if termo_limpo in receita.ingredientes:
                    resultados.append(receita)
                
                no_atual = no_atual.proximo

        return resultados
        
    def investigar_sabotagens(self) -> list:
        receitas_corrompidas = []

        for indice in range(self.capacidade):
            no_atual = self.tabela[indice]
           
            while no_atual:
                receita = no_atual.valor
                assinatura_atual = self.calcular_assinatura_receita(receita)
               
                if assinatura_atual != receita.assinatura_original:
                    receitas_corrompidas.append(receita)
               
                no_atual = no_atual.proximo

        return list(set(receitas_corrompidas))
    
    def obter_todas_receitas(self) -> list:
        todas = []
        
        for i in range(self.capacidade):
            no_atual = self.tabela[i]
            
            while no_atual is not None:
                todas.append(no_atual.valor)
                no_atual = no_atual.proximo
                
        return todas