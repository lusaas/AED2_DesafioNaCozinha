class MenuVip:
    def busca(self, ingrediente1, ingrediente2, ingredientes_estoque: dict, hash_sistema):
        receitas_com_ingrediente1 = hash_sistema.buscar_por_ingrediente(ingrediente1)
        receitas_disponiveis = []
        
        estoque_min = {k.lower().strip(): v for k, v in ingredientes_estoque.items()}
        term_ing2 = ingrediente2.lower().strip()

        for r in receitas_com_ingrediente1:
            ingredientes_normalizados = [ing.lower().strip() for ing in r.ingredientes]
            if term_ing2 in ingredientes_normalizados:
                pode_fazer = True
                
                for ing in r.ingredientes:
                    ing_limpo = ing.lower().strip()
                    if estoque_min.get(ing_limpo, 0) < 1:
                        pode_fazer = False
                        break
                    
                if pode_fazer:
                    receitas_disponiveis.append(r)

        if receitas_disponiveis:
            print(f"\nForam encontradas {len(receitas_disponiveis)} receitas que utilizam '{ingrediente1}' e '{ingrediente2}:")
            print("-" * 50)
            for r in receitas_disponiveis:
                print(f"  * {r.nome:<30} | Categoria: {r.categoria}")
            print("-" * 50)
            return
        else:
            print(f"\nNenhuma receita encontrada contendo os ingredientes '{ingrediente1}' e '{ingrediente2}.")
            return
        
    def maior_lucro (self, ingredientes_estoque, hash_sistema):
        todas_receitas = hash_sistema.obter_todas_receitas()
            
        estoque_simulado = {k.lower().strip(): v for k, v in ingredientes_estoque.items()}
                   
        receitas_candidatas = []
        for r in todas_receitas:
            preco = getattr(r, 'custo')
            qtd_ingredientes = len(r.ingredientes) if r.ingredientes else 1
            eficiencia = preco / qtd_ingredientes
                
            receitas_candidatas.append({
                "objeto": r,
                "preco": preco,
                "eficiencia": eficiencia
            })
            
        receitas_candidatas.sort(key=lambda x: x["eficiencia"], reverse=True)
            
        menu_sugerido = []
        lucro_total = 0.0
            
        for item in receitas_candidatas:
            r = item["objeto"]
            pode_produzir = True
                
            for ing in r.ingredientes:
                if estoque_simulado.get(ing, 0) < 1:
                    pode_produzir = False
                    break
                
            if pode_produzir:
                for ing in r.ingredientes:
                    estoque_simulado[ing] -= 1
                    
                menu_sugerido.append(r)
                lucro_total += item["lucro"]
            
        print("\n" + "="*55)
        print(f"{'SUGESTÃO DE MENU DE MAIOR LUCRO':^55}")
        print("="*55)
        if menu_sugerido:
            print("Combinação otimizada com base no seu estoque de agora:\n")
            for i, r in enumerate(menu_sugerido, 1):
                preco = getattr(r, 'preco', 50.0)
                custo = getattr(r, 'custo', 20.0)
                lucro = getattr(r, 'lucro', preco - custo)
                print(f"  {i}º. {r.nome:<30} | Lucro: R$ {lucro:.2f}")
            print("-"*55)
            print(f"  Total de pratos viáveis simultaneamente: {len(menu_sugerido)}")
            print(f"  Lucro Máximo Possível: R$ {lucro_total:.2f}")
        else:
            print("  Estoque insuficiente para produzir receitas completas.")
        print("="*55)
            
        return
