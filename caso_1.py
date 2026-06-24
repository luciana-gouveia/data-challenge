import pandas as pd
from sqlalchemy import create_engine

USER = "looqbox-challenge"
PASS = "looq-challenge"
IP = "35.199.115.174"
SCHEMA = "looqbox-challenge"
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASS}@{IP}/{SCHEMA}")

def retrieve_data(product_code=None, store_code=None, date=None):
    """
    Função dinâmica para buscar dados na tabela data_product_sales.
    Permite filtros opcionais por código do produto, código da loja e intervalo de datas.
    """
    # Query base usando o truque do WHERE 1=1 para concatenação limpa
    query = "SELECT * FROM data_product_sales WHERE 1=1"
    
    # Se o parâmetro foi enviado, adiciona à query
    if product_code is not None:
        query += f" AND PRODUCT_CODE = {product_code}"
        
    if store_code is not None:
        query += f" AND STORE_CODE = {store_code}"
        
    # Verifica se a data foi enviada e se possui os dois limites (início e fim)
    if date is not None and isinstance(date, list) and len(date) == 2:
        query += f" AND DATE BETWEEN '{date[0]}' AND '{date[1]}'"
        
    # Executa a query construída e retorna o dataframe
    print(f"Executando Query Dinâmica: {query}\n")
    df = pd.read_sql(query, con=engine)
    return df

# --- TESTANDO A FUNÇÃO ---
try:
    print("--- CASO 1: TESTANDO A FUNÇÃO DINÂMICA ---")
    

    meu_df = retrieve_data(date=['2019-01-01', '2019-01-05'])
    
    print("Primeiras linhas do DataFrame retornado:")
    print(meu_df.head())

except Exception as e:
    print("Erro ao executar a função:")
    print(e)