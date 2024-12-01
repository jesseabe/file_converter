import pandas as pd
import os
from typing import Optional

def xlsx_to_json(caminho: str, caminho_para_salvar: Optional[str] = None) -> None:
    try:
        # Read the excel file
        df = pd.read_excel(caminho)

        # Determine the save path if not provided
        if caminho_para_salvar is None:
            caminho_para_salvar = os.path.splitext(caminho)[0] + ".json"

        # Save to the specified or default json
        df.to_json(caminho_para_salvar, index=False)
        print(f"Arquivo convertido e salvo em {caminho_para_salvar}")

    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")
    
if __name__ == "__main__":
    xlsx_to_json("data/vendas.xlsx")