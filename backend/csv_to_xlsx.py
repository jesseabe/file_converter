import pandas as pd
import os
from typing import Optional

def csv_to_xlsx(caminho: str, caminho_para_salvar: Optional[str] = None) -> None:
    try:
        # Reading file
        df = pd.read_csv(caminho)

        if caminho_para_salvar is None:
            caminho_para_salvar = os.path.splitext(caminho)[0] + ".xlsx"

        # Save as excel 
        df.to_excel(caminho_para_salvar, index=False)
        print(f"Arquivo convertido e salvo em {caminho_para_salvar}")
    
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")

if __name__ == "__main__":
    csv_to_xlsx("data/vendas.csv", "data/vendas.xlsx")