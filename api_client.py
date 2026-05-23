import requests
import random
from receita import Receita

class MealDBService:
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1/"

    # MUDANÇA 1: Alterado o nome do método para bater com o que o main.py espera
    def buscar_receita_por_id(self, id_meal: str):
        """Busca a receita pelo seu ID estável e gera metadados fixos."""
        # MUDANÇA 2: Alterado o endpoint para buscar por ID (lookup.php?i=)
        url = f"{self.base_url}lookup.php?i={id_meal}"

        try:
            resposta = requests.get(url)
            dados = response = resposta.json()

            if not dados["meals"]:
                return None
            
            meal_data = dados["meals"][0]
            categoria = meal_data.get("strCategory", "").lower()

            # Trava o random com o ID da receita para gerar valores fixos
            random.seed(int(id_meal))

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
            random.seed(None)  # Reseta o gerador

            # Coleta de ingredientes
            ingredientes = []
            for i in range(1, 21):
                ingrediente = meal_data.get(f"strIngredient{i}")
                if ingrediente and ingrediente.strip():
                    ingredientes.append(ingrediente.strip().lower())

            # MUDANÇA 3: O return foi movido para fora do loop 'for' (alinhado com ele)
            # para que o Python leia todos os 20 ingredientes antes de criar a receita
            return Receita(
                id=int(id_meal),
                nome=meal_data["strMeal"],
                categoria=meal_data["strCategory"],
                tempo_preparo=tempo,
                avaliacao=avaliacao,
                custo=custo,
                ingredientes=ingredientes
            )
        
        except Exception as e:
            print(f"Erro ao conectar com a API para o ID {id_meal}: {e}")
            return None