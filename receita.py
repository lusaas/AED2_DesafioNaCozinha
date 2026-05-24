from dataclasses import dataclass, field
from typing import List

@dataclass
class Receita:
    id: int
    nome: str
    categoria: str
    tempo_preparo: int
    avaliacao: float
    custo: float
    ingredientes: List[str] = field(default_factory=list)

Ingredientes_adulterados = ["óleo de motor", "detergente ype", "laxante", "césio 137", "soda cáustica", "mosca", "cabelo"]
