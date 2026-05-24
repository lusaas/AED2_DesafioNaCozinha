# AED2_DesafioNaCozinha - Relatório Final
## Henrique dos Reis e Luísa Carvalho Böhm
**Link do Repositório GitHub:** [https://github.com/lusaas/AED2_DesafioNaCozinha](https://github.com/lusaas/AED2_DesafioNaCozinha)

## Sobre o Projeto
O "Desafio na Cozinha" é uma aplicação de linha de comandos desenvolvida em Python que atua como um Livro de Receitas Digital inteligente. O objetivo principal deste projeto é aplicar conceitos práticos de Algoritmos e Estruturas de Dados Avançadas (AED2) para solucionar problemas reais de armazenamento, indexação, pesquisa e otimização de consultas de dados.

## Instruções de Execução

**Pré-requisitos:**
- Python 3.8 ou superior instalado.
- Biblioteca `requests` instalada (caso deseje correr a atualização de dados da API).

**Passo a passo:**
1. Clone o repositório para a sua máquina local:
   ```bash
   git clone [https://github.com/lusaas/AED2_DesafioNaCozinha.git](https://github.com/lusaas/AED2_DesafioNaCozinha.git)
2.  Acesse à pasta do projeto: 

    cd AED2_DesafioNaCozinha

3.  Instale as dependências externas necessárias:

     pip install requests
4. Execute o ficheiro principal para iniciar o menu interativo:

    python main.py

## Fonte de Dados Escolhida:
A base de dados utilizada neste projeto foi extraída da API pública e global TheMealDB.
Para garantir a estabilidade nas simulações e permitir a execução offline, desenvolvemos um script de captura autónoma (capturar_dados.py) que extraiu 50 receitas fixas através dos seus IDs numéricos estáveis. Esses dados foram persistidos localmente no receitas_locais.json.

## Nota de Engenharia:
 Como a API original não fornece metadados cruciais para a lógica de negócio de restauração (tais como custo financeiro e tempo de preparação), o módulo api_client.py gera esses valores de forma determinística utilizando o ID único de cada receita como semente (random.seed). Isto garante que os custos, avaliações e tempos de uma determinada receita permaneçam estritamente idênticos e consistentes a cada execução do programa.
 
 ## Estruturas de Dados Implementadas
    Das opções teóricas estudadas ao longo do semestre, implementámos as seguintes estruturas avançadas com o foco em otimização de espaço e tempo:

**1. Árvore Trie (R-way)** 

Onde foi aplicada: Ficheiro arvore_trie.py e instanciada no fluxo de controlo do main.py.

Propósito: Responsável por armazenar e indexar os nomes das receitas e as suas categorias. Permite realizar consultas ultrarrápidas baseadas em prefixos (pesquisas instantâneas do tipo autocomplete, onde digitar "Ch" retorna imediatamente pratos que começam com "Chicken").

**2. Árvore Patrícia (Radix Tree / Compressão de Caminhos)** 
Onde foi aplicada: Ficheiro arvore_patricia.py (Acessível através do Modo Desafio no menu principal).

Propósito: Atua como um módulo avançado de otimização de memória. Esta estrutura recebe a Trie original de nomes e colapsa (comprime) sequencialmente todos os caminhos unidirecionais onde os nós intermédios possuem apenas um filho único. Isto mitiga radicalmente o desperdício de espaço e a sobrecarga de ponteiros nulos característicos da Trie clássica, mantendo a complexidade de tempo otimizada na procura.

**3.  Tabela Hash** 
Onde foi aplicada: Módulo tabela_hash.py (utilizado intensivamente em quase todas as opções do main.py).

Propósito: Utilizada para três finalidades de alta performance: Pesquisa direta de receitas pelo ID único com custo de tempo constante O(1), mapeamento invertido de ingredientes (para descobrir instantaneamente quais os pratos que utilizam um determinado ingrediente) e, fundamentalmente, na Varredura de Integridade (Modo Anti-Sabotagem), onde mapeia a assinatura dos objetos para validar que a base de dados não sofreu alterações maliciosas de "ingredientes adulterados" (ex: injeção de óleo de motor ou detergente ype).

## Algoritmos Escolhidos e Justificativas

modo_chef.py, implementámos algoritmos específicos para responder a requisitos analíticos do utilizador:

**1. Algoritmo de Ordenação: Merge Sort (_merge_sort_custo)**

Onde foi aplicado: Na ordenação de receitas pelo custo financeiro (ordem crescente).

Justificativa: O Merge Sort foi escolhido devido à sua complexidade de tempo firmemente garantida em O(n log n) tanto no melhor, médio, como no pior caso de distribuição de dados. Adicionalmente, por ser um algoritmo de ordenação estável, garante que pratos que possuam exatamente o mesmo custo financeiro mantenham a sua ordem de inserção original relativa, proporcionando uma apresentação estável e previsível de menus ao utilizador final.

**2. Algoritmo Guloso (Greedy Algorithm)**

Onde foi aplicado: Na função gerar_menu_economico dentro do "Modo Chef".

Justificativa: O problema modelado consiste em tentar colocar o maior número possível de pratos distintos dentro de um orçamento financeiro máximo estipulado pelo utilizador. A estratégia gulosa faz escolhas ótimas locais (selecionar e consumir sempre a receita mais barata disponível no topo da lista ordenada) sem necessidade de retrocesso (backtracking). Para este formato específico de maximização de cardinalidade (quantidade de itens), a aproximação gulosa é matematicamente ótima, extremamente leve em termos computacionais e ideal para execução em tempo real na interface.