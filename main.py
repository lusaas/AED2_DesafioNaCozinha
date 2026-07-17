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
from sistema_logistica import GrafoLogistica
from laboratorio_chef import LaboratorioChef

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
    
def inicializar_cenario_logistica(hash_sistema, estoque) -> GrafoLogistica:
    grafo_log = GrafoLogistica()
    
    grafo_log.adicionar_vertice("Cozinha_Central", "cozinha", capacidade=30)
    grafo_log.adicionar_vertice("Estacao_Auxiliar_Norte", "cozinha", capacidade=15)
    
    grafo_log.adicionar_vertice("Hub_Centro", "hub")
    grafo_log.adicionar_vertice("Hub_Leste", "hub")
    
    grafo_log.adicionar_vertice("Zona_Sul", "regiao")
    grafo_log.adicionar_vertice("Zona_Norte", "regiao")
    grafo_log.adicionar_vertice("Zona_Oeste", "regiao")

    grafo_log.adicionar_conexao("Cozinha_Central", "Hub_Centro", tempo=8.0, capacidade=25)
    grafo_log.adicionar_conexao("Cozinha_Central", "Hub_Leste", tempo=15.0, capacidade=12)
    grafo_log.adicionar_conexao("Estacao_Auxiliar_Norte", "Hub_Centro", tempo=12.0, capacidade=10)
    
    grafo_log.adicionar_conexao("Hub_Centro", "Zona_Sul", tempo=10.0, capacidade=15)
    grafo_log.adicionar_conexao("Hub_Centro", "Zona_Norte", tempo=14.0, capacidade=8)
    grafo_log.adicionar_conexao("Hub_Leste", "Zona_Norte", tempo=9.0, capacidade=10)
    grafo_log.adicionar_conexao("Hub_Leste", "Zona_Oeste", tempo=18.0, capacidade=15)

    for i in range(1, 13):
        nome_hub = f"Hub_Secundario_{i}"
        grafo_log.adicionar_vertice(nome_hub, "hub")
        
        tempo_cc = 10.0 + (i % 3)
        tempo_ean = 12.0 + (i % 4)
        grafo_log.adicionar_conexao("Cozinha_Central", nome_hub, tempo=tempo_cc, capacidade=8)
        grafo_log.adicionar_conexao("Estacao_Auxiliar_Norte", nome_hub, tempo=tempo_ean, capacidade=5)

    for j in range(1, 16):
        nome_regiao = f"Sub_Zona_{j}"
        grafo_log.adicionar_vertice(nome_regiao, "regiao")
        
        hub_origem_1 = f"Hub_Secundario_{((j) % 12) + 1}"
        hub_origem_2 = f"Hub_Secundario_{((j + 1) % 12) + 1}"
        
        grafo_log.adicionar_conexao(hub_origem_1, nome_regiao, tempo=7.0 + (j % 5), capacidade=10)
        grafo_log.adicionar_conexao(hub_origem_2, nome_regiao, tempo=9.0 + (j % 4), capacidade=8)

    grafo_log.adicionar_vertice("Super_Fonte", "auxiliar")
    grafo_log.adicionar_vertice("Super_Sumidouro", "auxiliar")
    
    grafo_log.adicionar_conexao("Super_Fonte", "Cozinha_Central", tempo=0.0, capacidade=30)
    grafo_log.adicionar_conexao("Super_Fonte", "Estacao_Auxiliar_Norte", tempo=0.0, capacidade=15)
    
    grafo_log.adicionar_conexao("Zona_Sul", "Super_Sumidouro", tempo=0.0, capacidade=20)
    grafo_log.adicionar_conexao("Zona_Norte", "Super_Sumidouro", tempo=0.0, capacidade=15)
    grafo_log.adicionar_conexao("Zona_Oeste", "Super_Sumidouro", tempo=0.0, capacidade=10)
    
    for j in range(1, 16):
        grafo_log.adicionar_conexao(f"Sub_Zona_{j}", "Super_Sumidouro", tempo=0.0, capacidade=12)

    return grafo_log

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
        print("11. Análise de Capacidade de Entregas")
        print("12. Descoberta Automática de Famílias Culinárias")
        print("13. Sair do Sistema")
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
            rede_logistica = inicializar_cenario_logistica(hash_sistema, ingredientes_estoque)
            
            print("\n" + "="*55)
            print(f"{'DESAFIO LOGÍSTICO: INTERLIGAÇÃO E ROTAS':^55}")
            print("="*55)
            print("PONTOS OPERACIONAIS DISPONÍVEIS:")
            for v_id, v in rede_logistica.vertices.items():
                if v.tipo != "auxiliar":
                    print(f"  • {v_id:<25} | Tipo: {v.tipo.upper()}")
            print("-" * 55)
            
            origem = input("Digite o ponto de origem: ").strip()
            destino = input("Digite o ponto de destino: ").strip()
            
            caminho, tempo_total = rede_logistica.calcular_rota_mais_rapida(origem, destino)
            
            if caminho:
                print("\nROTA RECOMENDADA (Menor tempo de tráfego):")
                print(" -> ".join(caminho))
                print(f"Tempo operacional estimado: {tempo_total:.1f} minutos.")
            else:
                print("\nNão foi possível traçar uma rota entre esses dois pontos.")
            print("="*55)

        elif opcao == "11":
            rede_logistica = inicializar_cenario_logistica(hash_sistema, ingredientes_estoque)
            
            fluxo_max, gargalos = rede_logistica.calcular_capacidade_maxima("Super_Fonte", "Super_Sumidouro")
            
            print("\n" + "="*55)
            print(f"{'ANÁLISE DE CAPACIDADE DE ENTREGA DA COZINHA':^55}")
            print("="*55)
            print(f"CAPACIDADE MÁXIMA DE ATENDIMENTO SIMULTÂNEO: {fluxo_max} pedidos")
            print("-" * 55)
            
            if gargalos:
                print("GARGALOS OPERACIONAIS DETECTADOS:")
                print("As seguintes rotas físicas operam em 100% da capacidade:")
                for g in gargalos:
                    # Oculta arestas auxiliares da exibição
                    if "Super" not in g[0] and "Super" not in g[1]:
                        print(f"Conexão: {g[0]} -> {g[1]} (Limite: {g[2]} pedidos/hora)")
            else:
                print("Não há gargalos ativos nas vias de transporte principais.")
            print("="*55)
            pass

        elif opcao == "12":
            lab = LaboratorioChef(hash_sistema)
            try:
                limiar = int(input("\nDigite o número mínimo de ingredientes compartilhados (ex: 2 ou 3): "))
                lab.identificar_familias_culinarias(limiar_minimo=limiar)
            except ValueError:
                print("Digite um número inteiro válido.")

        elif opcao == "13":
            print("\nEncerrando o sistema. Ate logo, Chef!")
            break
            
        else:
            print("\nOpcao invalida. Escolha de 1 a 8.")

if __name__ == "__main__":
    main()