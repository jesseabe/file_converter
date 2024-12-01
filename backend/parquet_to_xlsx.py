import pandas as pd
import os
from typing import Optional

def parquet_to_xlsx(caminho: str, caminho_para_salvar: Optional[str] = None) -> None:
    try:
        # Read the parquet file
        df = pd.read_parquet(caminho)

        # Determine the save path if not provided
        if caminho_para_salvar is None:
            caminho_para_salvar = os.path.splitext(caminho)[0] + ".xlsx"

        # Save to the specified or default xlsx
        df.to_excel(caminho_para_salvar, index=False)
        print(f"Arquivo convertido e salvo em {caminho_para_salvar}")

    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")
    
if __name__ == "__main__":
    parquet_to_xlsx("data/vendas.parquet")