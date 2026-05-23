from typing import List
from receita import Receita

class LivroReceitas:
    def __init__(self):
        self._receitas: List[Receita] = []

    def armazenar_receita(self, receita: Receita) -> bool:
        if not receita:
            return False

        for r in self._receitas:
            if r.id == receita.id:
                print(f"a receita '{receita.nome}' (ID: {receita.id}) já está no livro")
                return False
            
        self._receitas.append(receita)
        return True
    
    def listar_todas(self):
        if not self._receitas:
            print("\no livro está vazio")
            return
        
        print("\n" + "="*50)
        print(f"{'Livro de Receitas':^50}")
        print("="*50)

        for r in self._receitas:
            print(f"ID: {r.id:<6} | Nome: {r.nome} | Categoria: {r.categoria}")
            print(f"{r.tempo_preparo} min | {r.avaliacao} | R$ {r.custo:.2f}")
            print(f"Ingredientes ({len(r.ingredientes)}): {', '.join(r.ingredientes[:4])}...")
            print("-"*50)
        
        print(f"Total de receitas disponíveis: {len(self._receitas)}")
        print("="*50 + "\n")

    def buscar_por_id(self, id_busca: int) -> Receita:
        for r in self._receitas:
            if r.id == id_busca:
                return r
        return None

    def buscar_por_nome(self, nome_busca: str) -> List[Receita]:
        return [r for r in self._receitas if nome_busca.lower() in r.nome.lower()]