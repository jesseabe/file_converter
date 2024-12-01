import pandas as pd
import os

def csv_to_parquet(caminho, caminho_para_salvar=None):
    try:
        # Reading file
        df = pd.read_csv(caminho)

        if caminho_para_salvar is None:
            nome_arquivo = os.path.splitext(os.path.basename(caminho))[0]
            caminho_para_salvar = f"{nome_arquivo}.json"

        # Save as parquet 
        df.to_parquet(caminho_para_salvar, index=False, engine='pyarrow')
        print(f"Arquivo convertido e salvo em {caminho_para_salvar}")
    
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")

if __name__ == "__main__":
    csv_to_parquet("data/vendas.csv", "data/vendas.parquet")