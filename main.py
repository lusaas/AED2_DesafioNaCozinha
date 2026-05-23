import json
from receita import Receita
# Importando as estruturas de dados que VOCÊ vai construir do zero para a matéria:
from arvore_trie import ArvoreTrie
from tabela_hash import TabelaHash

def carregar_receitas_do_json(caminho_arquivo: str) -> list:
    """Lê o arquivo de backup local e transforma em objetos da classe Receita."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados_brutos = json.load(f)
        
        lista_receitas = []
        for meal_data in dados_brutos:
            id_meal = meal_data["idMeal"]
            
            # Simulando os metadados fixos através do ID (idêntico ao que fizemos antes)
            import random
            random.seed(int(id_meal))
            categoria = meal_data.get("strCategory", "").lower()
            
            if "dessert" in categoria:
                tempo = random.randint(15, 45)
                custo = round(random.uniform(10.0, 30.0), 2)
            elif "beef" in categoria or "pork" in categoria:
                tempo = random.randint(40, 120)
                custo = round(random.uniform(35.0, 80.0), 2)
            else:
                tempo = random.randint(20, 50)
                custo = round(random.uniform(20.0, 50.0), 2)
            
            avaliacao = round(random.uniform(3.5, 5.0), 1)
            random.seed(None) # Reseta o random

            # Coleta de ingredientes
            ingredientes = []
            for i in range(1, 21):
                ingrediente = meal_data.get(f"strIngredient{i}")
                if ingrediente and ingrediente.strip():
                    ingredientes.append(ingrediente.strip().lower())

            # Cria o objeto estável
            receita = Receita(
                id=int(id_meal),
                nome=meal_data["strMeal"],
                categoria=meal_data["strCategory"],
                tempo_preparo=tempo,
                avaliacao=avaliacao,
                custo=custo,
                ingredientes=ingredientes
            )
            lista_receitas.append(receita)
            
        return lista_receitas
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado. Execute o capturar_dados.py primeiro!")
        return []

def main():
    print("==================================================")
    print("       DESAFIO NA COZINHA - SISTEMA AED2          ")
    print("==================================================")

    # 1. Carrega os dados salvos localmente (Garantia de funcionamento offline)
    receitas_salvas = carregar_receitas_do_json("receitas_locais.json")
    if not receitas_salvas:
        return

    print(f"{len(receitas_salvas)} receitas carregadas com sucesso do arquivo local.")

    # 2. Inicializa as estruturas manuais obrigatórias pelo edital
    trie_nomes = ArvoreTrie()       # Técnica 1: Árvore Trie (para autocompletar/prefixos)
    hash_ingredientes = TabelaHash() # Técnica 2: Tabela Hash (para busca rápida e Modo Investigação)

    # 3. Alimenta as estruturas de dados com as receitas
    print("Indexando receitas nas estruturas de dados customizadas...")
    for r in receitas_salvas:
        trie_nomes.inserir(r.nome, r)
        hash_ingredientes.inserir(r.id, r)

    print("Estruturas prontas para consulta!\n")

    # ==================================================
    # Demonstração das Funcionalidades Exigidas no Edital
    # ==================================================
    
    # Teste da Árvore Trie (Modo Consulta Rápida por prefixo)
    print("[TESTE TRIE] Buscando receitas que começam com 'Ch':")
    resultados_trie = trie_nomes.buscar_por_prefixo("Ch")
    for receita in resultados_trie:
        print(f"  -> {receita.nome} ({receita.categoria})")

    print("-" * 50)

    # Teste da Tabela Hash (Modo Investigação / Busca por ID em O(1))
    print("[TESTE HASH] Buscando a receita de ID 52772 na nossa Tabela Hash:")
    receita_hash = hash_ingredientes.buscar(52772)
    if receita_hash:
        print(f"  -> Encontrada: {receita_hash.nome} | Custo: R$ {receita_hash.custo}")
    else:
        print("  -> Receita não encontrada na tabela.")

if __name__ == "__main__":
    main()