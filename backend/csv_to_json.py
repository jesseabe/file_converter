import pandas as pd
import os
from typing import Optional

def csv_to_json(caminho: str, caminho_para_salvar: Optional[str] = None) -> None:
    try:
        # Reading file
        df = pd.read_csv(caminho)

        if caminho_para_salvar is None:
            caminho_para_salvar = os.path.splitext(caminho)[0] + ".json"

        # Save as JSON
        df.to_json(caminho_para_salvar, orient='records', force_ascii=False)
        print(f"Arquivo convertido e salvo em {caminho_para_salvar}")
    
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")

if __name__ == "__main__":
    csv_to_json("data/vendas.csv", "data/vendas.json")



