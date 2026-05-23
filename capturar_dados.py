import requests
import json

def capturar_e_salvar_localmente():
    base_url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i="
    
    # Os 50 IDs estáveis que selecionamos
    ids_fixos = [
        "52767", "52768", "52769", "52770", "52772", "52773", "52774", "52775", "52776", "52777",
        "52824", "52826", "52874", "52875", "52878", "52994", "52995", "52996", "52997", "53000",
        "52795", "52796", "52818", "52819", "52820", "52846", "52850", "52879", "52934", "52940",
        "52771", "52802", "52821", "52836", "52859", "52882", "52918", "52944", "52953", "52959",
        "52779", "52780", "52811", "52844", "52848", "52893", "52906", "52929", "52955", "52971"
    ]
    
    lista_receitas_brutas = []
    print("Baixando e salvando cópia de segurança local das receitas...")
    
    for i, id_meal in enumerate(ids_fixos, 1):
        print(f"Baixando ({i}/50)...", end="\r")
        try:
            resposta = requests.get(f"{base_url}{id_meal}")
            dados = resposta.json()
            if dados and dados["meals"]:
                lista_receitas_brutas.append(dados["meals"][0])
        except Exception as e:
            print(f"\nErro ao baixar ID {id_meal}: {e}")
            
    with open("receitas_locais.json", "w", encoding="utf-8") as f:
        json.dump(lista_receitas_brutas, f, indent=4, ensure_ascii=False)
        
    print("\nArquivo 'receitas_locais.json' gerado com sucesso para uso offline!")

if __name__ == "__main__":
    capturar_e_salvar_localmente()