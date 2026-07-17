import json
import random
from receita import Receita
from receita import Ingredientes_adulterados
from arvore_trie import ArvoreTrie
from tabela_hash import TabelaHash
from modo_chef import ModuloChef
from arvore_patricia import ArvorePatricia
from dependencia import Grafo
from menu_vip import MenuVip

def carregar_receitas_do_json(caminho_arquivo: str) -> list:
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados_brutos = json.load(f)
        
        lista_receitas = []
        for meal_data in dados_brutos:
            id_meal = meal_data["idMeal"]
            
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
            random.seed(None)

            ingredientes = []
            for i in range(1, 21):
                ingrediente = meal_data.get(f"strIngredient{i}")
                if ingrediente and ingrediente.strip():
                    ingredientes.append(ingrediente.strip().lower())

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
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado. Execute 'capturar_dados.py' primeiro!")
        return []
    
def carregar_estoque(caminho_arquivo: str) -> dict:
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados_brutos = json.load(f)
        
        estoque = dados_brutos.get("ingredientes", {})
        return estoque
    
    except FileNotFoundError:
        print(f"ERRO: Arquivo de estoque '{caminho_arquivo}' não foi encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"ERRO: Falha ao decodificar o arquivo JSON.")
        return {}

def main():
    receitas_salvas = carregar_receitas_do_json("receitas_locais.json")
    ingredientes_estoque = carregar_estoque("estoque1.json")
    if not receitas_salvas:
        return

    trie_nomes = ArvoreTrie()       
    trie_categorias = ArvoreTrie()  
    hash_sistema = TabelaHash() 
    chef_guloso = ModuloChef(receitas_salvas)
    dependencias = Grafo()
    menu_vip = MenuVip()

    for r in receitas_salvas:
        trie_nomes.inserir(r.nome, r)
        trie_categorias.inserir(r.categoria, r) 
        hash_sistema.inserir(r.id, r)

    while True:
        print("\n" + "="*50)
        print(f"{'SISTEMA DESAFIO NA COZINHA (AED2)':^50}")
        print("="*50)
        print("1. Modo Consulta: Buscar por Prefixo do NOME (via TRIE)")
        print("2. Modo Consulta: Filtrar por Categoria (via TRIE)")
        print("3. Modo Consulta: Buscar por Ingrediente (via HASH)")
        print("4. Modo Consulta: Buscar por ID (via HASH)")
        print("5. Modo Investigação: Varredura Anti-Sabotagem (via HASH)")
        print("6. Modo Chef: Algoritmo Guloso (Menu Econômico)")
        print("7. [Desafio] Otimização de Memória: Compactar para Árvore Patrícia")
        print("8. Oficina de Produção")
        print("9. Menu VIP")
        print("10. Desafio Logístico")
        print("11. Sistema de Entregas")
        print("12. Sair do Sistema")
        print("="*50)
        
        opcao = input("Escolha o modo de interação: ")

        if opcao == "1":
            prefixo = input("\nDigite as primeiras letras do prato (ex: Ch, Ba, Sal): ")
            resultados = trie_nomes.buscar_por_prefixo(prefixo)
            print(f"\n{len(resultados)} correspondencia(s) encontrada(s):")
            for r in resultados:
                print(f"  * {r.nome} ({r.categoria})")

        elif opcao == "2":
            cat_busca = input("\nDigite a categoria desejada (ex: Beef, Chicken, Dessert, Pasta, Seafood): ")
            resultados = trie_categorias.buscar_por_prefixo(cat_busca)
            
            if resultados:
                print(f"\nForam encontradas {len(resultados)} receitas na categoria '{cat_busca}':")
                print("-" * 50)
                for r in resultados:
                    print(f"  * {r.nome:<30} | Tempo: {r.tempo_preparo} min | Custo: R$ {r.custo:.2f}")
                print("-" * 50)
            else:
                print(f"\nNenhuma receita encontrada para a categoria '{cat_busca}'.")

        elif opcao == "3":
            ing_busca = input("Digite o ingrediente para busca: ")
            resultados = hash_sistema.buscar_por_ingrediente(ing_busca)
            
            if resultados:
                print(f"\nForam encontradas {len(resultados)} receitas que utilizam '{ing_busca}':")
                print("-" * 50)
                for r in resultados:
                    print(f"  * {r.nome:<30} | Categoria: {r.categoria}")
                print("-" * 50)
            else:
                print(f"\nNenhuma receita encontrada contendo o ingrediente '{ing_busca}'.")

        elif opcao == "4":
            id_busca = input("\nDigite o ID numerico da receita (ex: 52772): ")
            if id_busca.isdigit():
                r = hash_sistema.buscar(int(id_busca))
                if r:
                    print(f"\nReceita Encontrada:\n  Nome: {r.nome}\n  Categoria: {r.categoria}\n  Avaliação: {r.avaliacao}\nCusto: R$ {r.custo}\n  Tempo: {r.tempo_preparo} min\n  Ingredientes: {', '.join(r.ingredientes)}")
                else:
                    print("\nID não encontrado na Tabela Hash.")
            else:
                print("\nPor favor, digite um ID numerico valido.")

        elif opcao == "5":
            print("\nIniciando varredura de integridade de dados...")
            sabotados = hash_sistema.investigar_sabotagens()
            if not sabotados:
                print("Tudo limpo! Nenhuma alteracao maldosa detectada.")
                
            else:
                print(f"ALERTA! DETECTAMOS {len(sabotados)} RECEITA(S) SABOTADA(S):")
                for r in sabotados:
                    print(f"  * PRATO VIOLADO: '{r.nome}' (ID: {r.id})")
            
            simular = input("\nDeseja fazer uma sabotagem para testar o sistema? (s/n): ")
            if simular.lower() == 's':
                receita_aleatoria = random.choice(receitas_salvas)
                id_aleatorio = receita_aleatoria.id
                receita_alvo = hash_sistema.buscar(id_aleatorio) 
                if receita_alvo:
                    ingrediente_sabotado = random.choice(Ingredientes_adulterados)
                    receita_alvo.ingredientes[0] = ingrediente_sabotado
                    print("Sabotagem injetada com sucesso.")
                    
        elif opcao == "6":
            try:
                orcamento = float(input("\nQuanto eh o orcamento maximo para o Menu (R$)? "))
                menu, custo_final = chef_guloso.gerar_menu_economico(orcamento)
               
                menu_para_exibir = list(menu)
                n = len(menu_para_exibir)
               
                for i in range(n):
                    indice_maior = i
                    for j in range(i + 1, n):
                        if menu_para_exibir[j].avaliacao > menu_para_exibir[indice_maior].avaliacao:
                            indice_maior = j
                    menu_para_exibir[i], menu_para_exibir[indice_maior] = menu_para_exibir[indice_maior], menu_para_exibir[i]
               
                print(f"\nSUGESTAO DO CHEF (Algoritmo Guloso - Exibido por Melhor Avaliacao):")
                print(f"Conseguimos colocar {len(menu_para_exibir)} pratos no seu menu sem estourar o limite!")
                print("-" * 65)
               
                for r in menu_para_exibir:
                    print(f"  * {r.nome:<30} | Nota: {r.avaliacao} | Custo: R$ {r.custo:.2f}")
                   
                print("-" * 65)
                print(f"Total Utilizado: R$ {custo_final:.2f} / Limite: R$ {orcamento:.2f}")
            except ValueError:
                print("\nDigite um valor numerico valido para o orçamento.")
                
        elif opcao == "7":
            print("\n" + "="*55)
            print(f"{'DESAFIO: COMPRESSÃO DE CAMINHOS (ÁRVORE PATRÍCIA)':^55}")
            print("="*55)
            print("Instanciando a Árvore Patrícia a partir da Trie original de nomes...")
            
            arvore_comprimida = ArvorePatricia(trie_nomes)
            
            arvore_comprimida.imprimir_arvore()
            
            print("\n" + "-"*55)
            print(f"{'PROVA DE FUNCIONAMENTO (BUSCA POR PREFIXO)':^55}")
            print("-"*55)
            prefixo_teste = input("Digite um prefixo (ex: 'ba' para Bakewell, 'ch' para Chicken): ").strip()
            
            resultados = arvore_comprimida.buscar_por_prefixo(prefixo_teste)
            
            if resultados:
                print(f"\n[Sucesso] Encontrada(s) {len(resultados)} receita(s) para o prefixo '{prefixo_teste}':")
                for r in resultados:
                    print(f" -> {r.nome} (Custo: R$ {r.custo:.2f})")
            else:
                print(f"\n[Aviso] Nenhuma receita encontrada com o prefixo '{prefixo_teste}'.")
            print("="*55)


        elif opcao == "8":
            while True:
                print("\n" + "="*50)
                print(f"{'OFICINA DE PRODUÇÃO':^50}")
                print("="*50)
                print("1. Cadastrar Dependências")
                print("2. Verificar Sequência Viável")
                print("3. Identificar Inconsistências")
                print("4. Ver Ordem Válida")
                print("5. Voltar")
                print("="*50)

                opcao = int(input("Digite a opção: "))
                
                if opcao == 1:
                    origem = int(input("Digite o ID da receita de ORIGEM da dependência: "))
                    destino = int(input("Digite o ID da receita de DESTINO da dependência: "))

                    dependencias.adiciona(origem, destino)

                    print(f"Foi adicionado a dependência entre '{origem}' -> '{destino}'\n")
                
                elif opcao == 2:
                    dependencias.imprime_grafo(hash_sistema)

                elif opcao == 3:
                    dependencias.identificar_inconsistencias(hash_sistema)

                elif opcao == 4:
                    dependencias.ordenar(hash_sistema)

                elif opcao == 5:
                    break

        elif opcao == "9":
            while True:
                print("\n" + "="*50)
                print(f"{'MENU VIP':^50}")
                print("="*50)
                print("1. Buscar Receitas por Ingredientes Disponíveis")
                print("2. Sugerir Menu de Maior Lucro")
                print("3. Voltar")
                print("="*50)

                opcao = int(input("Digite a opção: "))
                
                if opcao == 1:
                    ingrediente1 = input("Digite o nome do ingrediente 1: ").strip()
                    ingrediente2 = input("Digite o nome do ingrediente 2: ").strip()
                    
                    menu_vip.busca(ingrediente1, ingrediente2, ingredientes_estoque, hash_sistema)
                    
                elif opcao == 2:
                    menu_vip.maior_lucro(ingredientes_estoque, hash_sistema)

                elif opcao == 3:
                    break

        elif opcao == "10":
            pass

        elif opcao == "11":
            pass

        elif opcao == "12":
            print("\nEncerrando o sistema. Ate logo, Chef!")
            break
            
        else:
            print("\nOpcao invalida. Escolha de 1 a 8.")

if __name__ == "__main__":
    main()