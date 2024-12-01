import pandas as pd
import os

def csv_to_json(caminho, caminho_para_salvar=None):
    try:
        # Reading file
        df = pd.read_csv(caminho)

        if caminho_para_salvar is None:
            nome_arquivo = os.path.splitext(os.path.basename(caminho))[0]
            caminho_para_salvar = f"{nome_arquivo}.json"

        # Save as JSON
        df.to_json(caminho_para_salvar, orient='records', force_ascii=False)
        print(f"Arquivo convertido e salvo em {caminho_para_salvar}")
    
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")

if __name__ == "__main__":
    csv_to_json("data/vendas.csv", "data/vendas.json")
