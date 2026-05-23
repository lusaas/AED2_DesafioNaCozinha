from dataclasses import dataclass, field
from typing import List

@dataclass
class Receita:
    nome: str
    id: int
    categoria: str
    tempo_preparo: int
    ingredientes: List[str] = field(default_factory=list)
    preco: float

class GerenciadorRestaurante:
    def __init__(self):
        self.receitas = []

    def adiciona_receita:
        self.receitas.append(receita)
    
    def busca_nome(self, nome:str):
        return [r for r in self.receitas if nome.lower() in r.nome.lower()]
    
    def busca_id(self, id_busca:int):
        for r in self.receitas:
            if r.id == id_busca:
                return r 
        return None
