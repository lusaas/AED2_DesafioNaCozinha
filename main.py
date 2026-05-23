from gerenciador import LivroReceitas
from api_client import MealDBService

def main():
    # Inicializa os módulos do sistema
    livro = LivroReceitas()
    api = MealDBService()

    print("=== Inicializando Módulo 1: Livro de Receitas ===")
    
    pratos_para_buscar = ["Arrabiata", "Burger", "Wonton Soup"]

    print("\nBuscando pratos na API do TheMealDB...")
    for nome in pratos_para_buscar:
        receita_api = api.buscar_receita_por_nome(nome)
        if receita_api:
            livro.armazenar_receita(receita_api)
        else:
            print(f"Não foi possível encontrar: {nome}")

    livro.listar_todas()

    print("--- Testando Busca por Nome: 'burger' ---")
    resultados = livro.buscar_por_nome("burger")
    for r in resultados:
        print(f"Encontrado: {r.nome} (ID: {r.id})")

if __name__ == "__main__":
    main()