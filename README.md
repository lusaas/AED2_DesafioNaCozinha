# AED2 DesafioNaCozinha - Relatório Final
**DESAFIO NA COZINHA**

* **Autores:** Henrique dos Reis & Luísa Carvalho Böhm
* **Disciplina:** Algoritmos e Estruturas de Dados Avançadas II (AED2)
* **Data:** 20 de Julho de 2026
* **GitHub:** [github.com/lusaas/AED2_DesafioNaCozinha](https://github.com/lusaas/AED2_DesafioNaCozinha)

---

## 1. Sobre o Projeto e Arquivos de Dados

O **Desafio na Cozinha** é uma aplicação de linha de comando (CLI) construída em Python que atua como um ecossistema completo de gestão e otimização gastronômica[cite: 7]. O sistema resolve problemas reais de indexação de receitas, detecção de adulterações, planejamento financeiro guloso, encadeamento de dependências de preparo, rotas de entrega urbana, capacidade de fluxo logístico máximo e agrupamento de famílias de pratos por similaridade de ingredientes.

### Arquivos de Dados e Persistência Local
* **`receitas_locais.json`**: Base principal contendo 50 receitas fixas capturadas de forma autônoma da API global *TheMealDB* via `capturar_dados.py`. Para assegurar reprodutibilidade offline, atributos de custo financeiro (R$), tempo de preparo e avaliação são gerados deterministicamente usando o `idMeal` numérico como semente (`random.seed`).
* **`estoque1.json`**: Arquivo de banco local contendo o inventário quantitativo de ingredientes disponíveis na dispensa do restaurante para alimentação do Menu VIP e algoritmo guloso.
* **`lista_id_receitas.txt` e `categorias_e_ingredientes.txt`**: Ficheiros de auxílio rápido contendo os mapeamentos diretos de IDs, categorias e ingredientes para fácil consulta e validação durante a navegação.

---

## 2. Instruções de Execução

### Pré-requisitos
* Python 3.8 ou superior instalado no ambiente.
* Biblioteca `requests` instalada (necessária apenas para atualizar os dados via API externa).

### Passo a Passo de Instalação e Execução
```bash
# 1. Clonar o repositório oficial
git clone [https://github.com/lusaas/AED2_DesafioNaCozinha.git](https://github.com/lusaas/AED2_DesafioNaCozinha.git)

# 2. Acessar a pasta do projeto
cd AED2_DesafioNaCozinha

# 3. Instalar dependências externas
pip install requests

# 4. Executar o sistema principal
python main.py
```

---

## 3. Relatório Técnico: Estruturas de Dados e Algoritmos

Abaixo apresenta-se a justificativa teórica, complexidade computacional e adequação ao problema para cada estrutura e algoritmo implementado.

| Módulo / Recurso | Estrutura / Algoritmo | Complexidade Temporal | Complexidade Espacial | Justificativa e Adequação Técnica |
| :--- | :--- | :--- | :--- | :--- |
| **Busca por Autocomplete** | Árvore Trie (R-Way) | Procura: $O(L)$<br>Inserção: $O(L)$ | $O(N \cdot L \cdot \Sigma)$ | Permite busca instantânea por prefixo independente do volume total de receitas. O tempo de busca depende apenas do tamanho da palavra chave ($L$). |
| **Otimização de Memória** | Árvore Patrícia (Radix Tree) | Procura: $O(L)$<br>Compressão: $O(N \cdot L)$ | $O(N \cdot L)$ | Colapsa nós unidirecionais encadeados. Reduz drasticamente a sobrecarga de ponteiros nulos da Trie tradicional, otimizando o consumo de RAM. |
| **Acesso Direto e Anti-Sabotagem** | Tabela Hash com Encadeamento | Busca ID: $O(1)$<br>Varredura: $O(N)$ | $O(N + M)$ | Garante acesso em tempo constante por ID, mapeia o índice invertido de ingredientes e realiza a auditoria de integridade contra injeção de itens adulterados. |
| **Menu Econômico e Menu VIP** | Merge Sort + Algoritmo Guloso (Greedy) | Ordenação: $O(N \log N)$<br>Seleção: $O(N \cdot I)$ | $O(N)$ | Garante ordenação estável por eficiência ($\text{Custo}/\text{Ingredientes}$). A escolha gulosa maximiza a cardinalidade/lucro no orçamento sem backtracking. |
| **Oficina de Produção (Pré-Req)** | Grafo Dirigido (DFS + Ordenação Topológica) | Detecção Ciclo: $O(V + E)$<br>Ord. Topológica: $O(V + E)$ | $O(V + E)$ | Mapeia dependências de pratos. Detecta travamentos cíclicos de preparação via estados de coloração da DFS e gera a sequência linear viável de cozimento. |
| **Desafio Logístico (Menor Tempo)** | Grafo Ponderado + Algoritmo de Dijkstra | Busca Rota: $O(V^2)$ ou $O((V+E)\log V)$ | $O(V + E)$ | Garante o caminho de menor tempo de tráfego urbano entre cozinhas, hubs e regiões de entrega, relaxando as arestas de vias ponderadas por minutos. |
| **Capacidade de Entrega Simultânea** | Rede de Fluxo + Algoritmo de Edmonds-Karp | Fluxo Máximo: $O(V \cdot E^2)$ | $O(V + E)$ | Mapeia gargalos operacionais e determina a capacidade máxima de atendimento simultâneo via busca em largura (BFS) em caminhos aumentantes entre Super-Fonte e Super-Sumidouro. |
| **Famílias Culinárias (Comunidades)** | Grafo Não-Dirigido + Busca em Largura (BFS) | Montagem: $O(N^2 \cdot I)$<br>BFS: $O(V + E)$ | $O(V + E)$ | Agrupa receitas que compartilham ingredientes acima de um limiar. Isola componentes conexos em grupos familiares de forma concêntrica. |

### Detalhamento dos Conceitos Teóricos Notáveis
* **Super-Fonte ($s$) e Super-Sumidouro ($t$):** Vértices virtuais introduzidos na rede de logística para transformar um problema de múltiplas cozinhas e múltiplos bairros em uma rede de fluxo de par único exigida pelo modelo de Ford-Fulkerson / Edmonds-Karp.
* **Componentes Conexos vs. Fortemente Conexos:** As Famílias Culinárias utilizam grafos não-dirigidos (simétricos), formando componentes conexos simples identificados via BFS. Já o módulo de Dependências utiliza digrafos, onde a detecção de ciclos requer controle rigoroso de estados na DFS.

---

## 4. Apresentação do Sistema Funcionando (Demonstração dos Módulos)

### MENU PRINCIPAL DO SISTEMA (`main.py`)
```text
==================================================
        SISTEMA DESAFIO NA COZINHA (AED2)
==================================================
1. Modo Consulta: Buscar por Prefixo do NOME (via TRIE)
2. Modo Consulta: Filtrar por Categoria (via TRIE)
3. Modo Consulta: Buscar por Ingrediente (via HASH)
4. Modo Consulta: Buscar por ID (via HASH)
5. Modo Investigação: Varredura Anti-Sabotagem (via HASH)
6. Modo Chef: Algoritmo Guloso (Menu Economico)
7. [Desafio] Otimização de Memória: Compactar para Árvore Patricia
8. Oficina de Produção
9. Menu VIP
10. Desafio Logistico
11. Análise de Capacidade de Entregas
12. Descoberta Automática de Familias Culinárias
13. Sair do Sistema
```

### Demonstração Módulo 8 — Oficina de Produção (Dependências & Ordenação Topológica)
```text
--- Executando Ordenação Topológica de Preparo
=======================================================
                     Preparo ideal
=======================================================
1º: Componente Base (ID 52772)
        ▼
2º: Teriyaki Chicken Casserole
        ▼
3º: Rigatoni with Chicken and Mushrooms (Conclusão do Fluxo)
```

### Demonstração Módulo 11 — Análise de Capacidade de Entregas (Edmonds-Karp)
```text
--- Cálculo de Fluxo Máximo e Gargalos Operacionais
=======================================================
       ANÁLISE DE CAPACIDADE DE ENTREGA DA COZINHA
=======================================================
CAPACIDADE MAXIMA DE ATENDIMENTO SIMULTANEO: 45 pedidos
-------------------------------------------------------
GARGALOS OPERACIONAIS DETECTADOS:
As seguintes rotas fisicas operam em 100% da capacidade:
 • Conexão: Cozinha_Central -> Hub_Centro (Limite: 25 pedidos/hora)
 • Conexão: Hub_Centro -> Zona_Sul (Limite: 15 pedidos/hora)
=======================================================
```

### Demonstração Módulo 12 — Famílias Culinárias (BFS em Grafo de Similaridade)
```text
--- Identificação de Comunidades Gastronômicas
=======================================================
    LABORATÓRIO DO CHEF: COMUNIDADES GASTRONÔMICAS
=======================================================
Analisando interconexões de ingredientes entre 50 receitas...
Limiar de corte adotado: minimo 3 ingredientes iguais.
-------------------------------------------------------
Familia Culinária #1 (3 pratos altamente relacionados):
Ingredientes de conexão: beef stock, salt, butter
    • Beef and Oyster pie  | Categoria: Beef
    • Beef and Mustard Pie | Categoria: Beef
    • French Onion Chicken | Categoria: Chicken
```